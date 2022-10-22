from pydantic import BaseSettings


class DatabaseConfig(BaseSettings):
    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:somepassword@localhost:5432/books_shop_sample"
    )
