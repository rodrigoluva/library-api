import asyncio

import typer
from sqlalchemy import select

from library_api.core.database import AsyncSessionLocal
from library_api.core.security import get_password_hash
from library_api.models.users import User, UserRole


app = typer.Typer()


@app.callback()
def main():
    """Library API CLI"""
    pass


@app.command(
        name='create-admin-user',
)
def create_admin_user(
        name: str = typer.Option(
            ...,
            prompt=True
        ),
        email: str = typer.Option(
            ...,
            prompt=True
        ),
        password: str = typer.Option(
            ...,
            prompt=True,
            confirmation_prompt=True,
            hide_input=True
        ),
):
    asyncio.run(
        create_admin_user_async(
            name=name,
            email=email,
            password=password,
        )
    )


async def create_admin_user_async(
        name: str,
        email: str,
        password: str,
):
    async with AsyncSessionLocal() as db:
        user_exists = await db.scalar(
            select(User)
            .where(User.email == email)
        )

        if user_exists:
            typer.echo('User already exists.')
            raise typer.Exit(code=1)
        
        user = User(
            email=email,
            password=get_password_hash(password),
            name=name,
            role=UserRole.ADMIN,
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        typer.echo(f'Created admin user {user.email} with id {user.id}')


@app.command(
        name='create-librarian-user',
)
def create_librarian_user(
        name: str = typer.Option(
            ...,
            prompt=True
        ),
        email: str = typer.Option(
            ...,
            prompt=True
        ),
        password: str = typer.Option(
            ...,
            prompt=True,
            confirmation_prompt=True,
            hide_input=True
        ),
):
    asyncio.run(
        create_librarian_user_async(
            name=name,
            email=email,
            password=password,
        )
    )


async def create_librarian_user_async(
        name: str,
        email: str,
        password: str,
):
    async with AsyncSessionLocal() as db:
        user_exists = await db.scalar(
            select(User)
            .where(User.email == email)
        )

        if user_exists:
            typer.echo('User already exists.')
            raise typer.Exit(code=1)
        
        user = User(
            email=email,
            password=get_password_hash(password),
            name=name,
            role=UserRole.LIBRARIAN,
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        typer.echo(f'Created librarian user {user.email} with id {user.id}')



if __name__ == '__main__':
    app()
