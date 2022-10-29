from blacksheep.server.controllers import APIController, post
from blacksheep import Response, FromJSON
from blacksheep.server.authorization import auth
from pydantic import BaseModel

from src.business_logic.create_book_service import CreateBookService


class CreateBook(BaseModel):
    title: str
    description: str
    price: float
    genre: str
    author_full_name: str = "Asd sDASD"


class Books(APIController):
    @auth("authenticated")
    @post("/")
    async def create_book(
        self, body: FromJSON[CreateBook], service: CreateBookService
    ) -> Response:
        await service.execute(
            title=body.value.title,
            description=body.value.description,
            author_full_name=body.value.author_full_name,
            price=body.value.price,
            genre=body.value.genre,
        )

        return Response(status=200)
