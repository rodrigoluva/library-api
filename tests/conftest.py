import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)

from library_api.app import app
from library_api.core.database import get_session
from library_api.core.security import get_password_hash
from library_api.models import Base
from library_api.models.users import User, UserRole


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
async def user(session, user_data):
    hashed_password = get_password_hash(user_data['password'])
    db_user = User(
        email=user_data['email'],
        password=hashed_password,
        name=user_data['name'],
        role=user_data['role'],
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user
