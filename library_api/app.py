from fastapi import FastAPI, status

from library_api.routers import (
    auth,
    authors,
    books,
    book_copies,
    users,
)


app = FastAPI()

app.include_router(
    router=auth.router,
    prefix='/api/v1',
    tags=['authentication'],
)

app.include_router(
    router=users.router,
    prefix='/api/v1/users',
    tags=['users'],
)

app.include_router(
   router=authors.router,
   prefix='/api/v1/authors',
   tags=['authors'],
)

app.include_router(
    router=books.router,
    prefix='/api/v1/books',
    tags=['books'],
)

app.include_router(
    router=book_copies.router,
    prefix='/api/v1',
    tags=['book-copies']
)

@app.get('/health_check', status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "200 OK"}
