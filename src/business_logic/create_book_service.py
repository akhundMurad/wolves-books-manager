from datetime import datetime

from src.business_logic.protocols.database_client import DatabaseClientProtocol


class CreateBookService:
    def __init__(self, database_client: DatabaseClientProtocol) -> None:
        self._database_client = database_client

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
            statement = """
            INSERT INTO books(title, description, author_full_name, genre, price, created_at)
            VALUES(:title, :description, :author_full_name, :genre, :price, :created_at)
            """
            await db.execute(
                statement,
                title=title,
                description=description,
                genre=genre,
                author_full_name=author_full_name,
                price=price,
                created_at=datetime.utcnow(),
            )

            await db.commit()
