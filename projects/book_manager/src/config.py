from pydantic import BaseSettings


class DatabaseConfig(BaseSettings):
    DATABASE_URL: str


class JWTConfig(BaseSettings):
    JWT_KEY: str = "asd"
    JWT_ALGORITHM: str = "HS256"


class MessageBrokerConfig(BaseSettings):
    MESSAGE_BROKER_URL: str
