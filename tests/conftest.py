from datetime import UTC, datetime, timedelta

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import selectinload

from library_api.app import app
from library_api.core.database import get_session
from library_api.core.security import create_access_token, get_password_hash
from library_api.models import Base
from library_api.models.books import (
    Author,
    Book,
    BookCopy,
    BookStatus,
    BorrowRecord,
)
from library_api.models.users import User, UserRole
from library_api.schemas.authors import AuthorSchema
from library_api.schemas.book_copies import BookCopyCreateSchema
from library_api.schemas.books import BookSchema
from library_api.schemas.users import UserSchema


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(url='sqlite+aiosqlite:///:memory:')

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def user_data():
    return {
        'email': 'test@test.com',
        'password': 'secret',
        'name': 'john',
        'role': UserRole.MEMBER,
    }


@pytest_asyncio.fixture
async def user_2_data():
    return {
        'email': 'test2@test.com',
        'password': 'secret2',
        'name': 'john 2',
        'role': UserRole.MEMBER,
    }


@pytest_asyncio.fixture
async def user_data_schema(user_data):
    return UserSchema(
        email=user_data['email'],
        password=user_data['password'],
        name=user_data['name'],
    )


@pytest_asyncio.fixture
async def user_2_data_schema(user_2_data):
    return UserSchema(
        email=user_2_data['email'],
        password=user_2_data['password'],
        name=user_2_data['name'],
    )


@pytest_asyncio.fixture
async def user(session, user_data_schema):
    hashed_password = get_password_hash(user_data_schema.password)
    db_user = User(
        email=user_data_schema.email,
        password=hashed_password,
        name=user_data_schema.name,
        role=UserRole.MEMBER,
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


@pytest_asyncio.fixture
async def user_2(session, user_2_data_schema):
    hashed_password = get_password_hash(user_2_data_schema.password)
    db_user = User(
        email=user_2_data_schema.email,
        password=hashed_password,
        name=user_2_data_schema.name,
        role=UserRole.MEMBER,
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


@pytest_asyncio.fixture
async def admin_user(session):
    user = User(
        name='Admin',
        email='admin@test.com',
        password=get_password_hash('test123'),
        role=UserRole.ADMIN,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@pytest.fixture
def user_token(user):
    return create_access_token(data={'sub': str(user.id)})


@pytest.fixture
def user_2_token(user_2):
    return create_access_token(data={'sub': str(user_2.id)})


@pytest.fixture
def admin_token(admin_user):
    return create_access_token(data={'sub': str(admin_user.id)})


@pytest.fixture
def author_schema():
    return AuthorSchema(
        name='george orwell',
        bio='English novelist',
        birthdate='1903-06-25',
    )


@pytest_asyncio.fixture
async def author(session, author_schema):
    db_author = Author(
        name=author_schema.name,
        bio=author_schema.bio,
        birthdate=author_schema.birthdate,
    )
    session.add(db_author)
    await session.commit()
    await session.refresh(db_author)

    return db_author


@pytest.fixture
def book_schema(author):
    return BookSchema(
        title='1984',
        isbn='9780451524935',
        published_date='1949-06-08',
        author_id=author.id,
    )


@pytest.fixture
def book_schema_2(author):
    return BookSchema(
        title='1984 2nd ed',
        isbn='9780451524930',
        published_date='1949-06-08',
        author_id=author.id,
    )


@pytest_asyncio.fixture
async def book(session, book_schema):
    db_book = Book(
        title=book_schema.title,
        isbn=book_schema.isbn,
        published_date=book_schema.published_date,
        author_id=book_schema.author_id,
    )

    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)

    return db_book


@pytest_asyncio.fixture
async def book_2(session, book_schema_2):
    db_book = Book(
        title=book_schema_2.title,
        isbn=book_schema_2.isbn,
        published_date=book_schema_2.published_date,
        author_id=book_schema_2.author_id,
    )

    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)

    return db_book


@pytest.fixture
def book_copies_schema(book):
    return BookCopyCreateSchema(
        quantity=2,
    )


@pytest_asyncio.fixture
async def book_copies(session, book, book_copies_schema):
    copies = [
        BookCopy(
            book_id=book.id,
            status=BookStatus.AVAILABLE,
        )
        for _ in range(book_copies_schema.quantity)
    ]

    session.add_all(copies)
    await session.commit()

    book_copies_result = await session.execute(
        select(BookCopy)
        .options(selectinload(BookCopy.book).selectinload(Book.author))
        .where(BookCopy.book_id == book.id)
        .order_by(BookCopy.id.desc())
        .limit(book_copies_schema.quantity)
    )
    created_copies = list(reversed(book_copies_result.scalars().all()))

    return {'copies': created_copies, 'quantity': book_copies_schema.quantity}


@pytest_asyncio.fixture
async def book_copy(session, book):
    copy = BookCopy(
        book_id=book.id,
        status=BookStatus.AVAILABLE,
    )

    session.add(copy)
    await session.commit()
    await session.refresh(copy)

    return copy


@pytest_asyncio.fixture
async def borrowed_record(session, user, book_copy):
    borrow_record = BorrowRecord(
        user_id=user.id,
        book_copy_id=book_copy.id,
        borrowed_at=datetime.now(UTC),
        due_at=datetime.now(UTC) + timedelta(days=14),
    )

    book_copy.status = BookStatus.BORROWED

    session.add(borrow_record)
    await session.commit()
    await session.refresh(borrow_record)

    return borrow_record
