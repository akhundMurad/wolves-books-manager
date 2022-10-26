from pydantic import BaseSettings


class DatabaseConfig(BaseSettings):
    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:somepassword@localhost:5432/books_sample"
    )


class JWTConfig(BaseSettings):
    JWT_KEY: str = "asd"
    JWT_ALGORITHM: str = "HS256"


class MessageBrokerConfig(BaseSettings):
    CONNECTION_STRING: str = "amqp://guest:guest@localhost/"
