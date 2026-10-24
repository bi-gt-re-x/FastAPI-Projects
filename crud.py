from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published_date: int = Field(ge=1800)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Book of Thrones",
                "author": "Author 1",
                "description": "Book 1",
                "rating": 1,
                "published_date": 1987
            }
        }
    }


BOOKS = [
    Book(1, 'Computer Science Pro', 'Roby McGart', 'A very nice book!', 5, 2020),
    Book(2, 'Be Fast with FastAPI', 'Roby McGart', 'A great book!', 5, 2021),
    Book(3, 'Master Endpoints', 'Roby McGart', 'A awesome book!', 5, 2022),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 1997),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 1998),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 1999),
    Book(7, 'Async Python Deep Dive', 'John Doe', 'Learn concurrency in Python.', 4, 2023),
    Book(8, 'Data Structures Blueprint', 'Jane Smith', 'Master core CS concepts.', 5, 2024),
    Book(9, 'Web Dev Essentials', 'Alex Green', 'A complete guide to modern web.', 3, 2025)
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book

    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(ge=1, le=5)):
    book_result = []
    for book in BOOKS:
        if book.rating == book_rating:
            book_result.append(book)

    return book_result

@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request =  BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    id = 1 if not BOOKS else BOOKS[-1].id + 1
    return book

@app.put("/books/update", status_code=status.HTTP_200_OK)
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            return

    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break

    if book_changed == False:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/books/{published_date}", status_code=status.HTTP_200_OK)
async def read_book_by_published_date(published_date: int = Query(ge=1800)):
    for book in BOOKS:
        if book.published_date == published_date:
            return book




















