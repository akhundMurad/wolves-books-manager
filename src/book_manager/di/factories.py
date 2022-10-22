from aio_pika import Connection, connect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from rodi import GetServiceContext

from book_manager.business_logic.create_book_service import CreateBookService
from book_manager.business_logic.protocols.database_client import DatabaseClientProtocol
from book_manager.business_logic.protocols.producer import ProducerProtocol
from book_manager.config import DatabaseConfig, JWTConfig, MessageBrokerConfig
from book_manager.data_access.persistence.database_client import DatabaseClient
from book_manager.data_access.producer.rabbitmq import Producer
from book_manager.presentation.api.auth import JWTManager


def build_database_config(context: GetServiceContext) -> DatabaseConfig:
    return DatabaseConfig()


def build_jwt_config(context: GetServiceContext) -> JWTConfig:
    return JWTConfig()


def build_message_broker_config(context: GetServiceContext) -> MessageBrokerConfig:
    return MessageBrokerConfig()


def build_sa_engine(context: GetServiceContext) -> AsyncEngine:
    database_config: DatabaseConfig = context.provider[DatabaseConfig]
    return create_async_engine(database_config.DATABASE_URL)


def build_sa_sessionmaker(context: GetServiceContext) -> sessionmaker:
    engine: AsyncEngine = context.provider[AsyncEngine]
    return sessionmaker(
        engine, class_=AsyncSession, autocommit=False, expire_on_commit=False
    )


def build_database_client(context: GetServiceContext) -> DatabaseClient:
    session_factory: sessionmaker = context.provider[sessionmaker]
    return DatabaseClient(session_factory)


def build_create_book_service(context: GetServiceContext) -> CreateBookService:
    database_client: DatabaseClientProtocol = context.provider[DatabaseClientProtocol]
    producer: ProducerProtocol = context.provider[ProducerProtocol]

    return CreateBookService(database_client=database_client, producer=producer)


def build_jwt_manager(context: GetServiceContext) -> JWTManager:
    config: JWTConfig = context.provider[JWTConfig]

    return JWTManager(key=config.JWT_KEY, algorithm=config.JWT_ALGORITHM)


def build_rabbitmq_producer(context: GetServiceContext) -> Producer:
    config: MessageBrokerConfig = context.provider[MessageBrokerConfig]

    return Producer(connection_string=config.CONNECTION_STRING)
