from datetime import datetime
from uuid import uuid4

from src.business_logic.protocols.database_client import DatabaseClientProtocol
from src.business_logic.protocols.producer import ProducerProtocol


class CreateBookService:
    def __init__(
        self, database_client: DatabaseClientProtocol, producer: ProducerProtocol
    ) -> None:
        self._database_client = database_client
        self._producer = producer

    async def execute(
        self,
        *,
        title: str,
        description: str,
        author_full_name: str,
        genre: str,
        price: float
    ) -> None:
        async with self._database_client as db:
            book = dict(
                id=uuid4(),
                title=title,
                description=description,
                genre=genre,
                author_full_name=author_full_name,
                price=price,
                created_at=datetime.utcnow(),
            )
            statement = """
            INSERT INTO books(id, title, description, author_full_name, genre, price, created_at)
            VALUES(:id, :title, :description, :author_full_name, :genre, :price, :created_at)
            """
            await db.execute(statement, **book)

            await db.commit()

            await self._producer.publish(message=book, exchange_name="books")
