from pydantic import BaseSettings


class DatabaseConfig(BaseSettings):
    DATABASE_URL: str

class MessageBrokerConfig(BaseSettings):
    MESSAGE_BROKER_URL: str
