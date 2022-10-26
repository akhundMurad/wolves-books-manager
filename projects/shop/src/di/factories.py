from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from rodi import GetServiceContext

from src.business_logic.books.service.create_book_service import CreateBookService
from src.business_logic.orders.service.create_order_service import CreateOrderService
from src.business_logic.protocols.database_client import DatabaseClientProtocol
from src.config import DatabaseConfig, MessageBrokerConfig
from src.data_access.persistence.database_client import DatabaseClient
from src.data_access.consumer.rabbitmq import Consumer


def build_database_config(context: GetServiceContext) -> DatabaseConfig:
    return DatabaseConfig()


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

    return CreateBookService(database_client=database_client)


def build_rabbitmq_consumer(context: GetServiceContext) -> Consumer:
    config: MessageBrokerConfig = context.provider[MessageBrokerConfig]
    service: CreateBookService = context.provider[CreateBookService]

    return Consumer(connection_string=config.CONNECTION_STRING, service=service)


def build_create_order_service(context: GetServiceContext) -> CreateOrderService:
    database_client: DatabaseClientProtocol = context.provider[DatabaseClientProtocol]

    return CreateOrderService(database_client=database_client)
