import pytest
from sqlalchemy import select

from library_api.models.users import User, UserRole


@pytest.mark.asyncio
async def test_create_user(session):
    new_user = User(
        email='test@test.com',
        password='secret',
        name='john',
        role=UserRole.MEMBER,
    )
    session.add(new_user)
    await session.commit()

    user = await session.scalar(
        select(User).where(User.email == 'test@test.com')
    )

    new_user_data = {
        'id': user.id,
        'email': user.email,
        'password': user.password,
        'name': user.name,
        'role': user.role,
    }

    assert new_user_data == {
        'id': 1,
        'email': 'test@test.com',
        'password': 'secret',
        'name': 'john',
        'role': UserRole.MEMBER,
    }
