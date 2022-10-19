from uuid import UUID
from pydantic import BaseModel, Field


class CreateOrderedBooks(BaseModel):
    book_id: UUID
    quantity: int


class CreateOrderCommand(BaseModel):
    books: list[CreateOrderedBooks] = Field(...)
    customer: UUID = Field(...)
