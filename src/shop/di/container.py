from rodi import Container
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from shop.business_logic.books.service.create_book_service import CreateBookService
from shop.business_logic.orders.service.create_order_service import CreateOrderService
from shop.business_logic.protocols.consumer import ConsumerProtocol

from shop.config import DatabaseConfig, MessageBrokerConfig
from shop.di.factories import (
    build_create_book_service,
    build_create_order_service,
    build_database_client,
    build_database_config,
    build_message_broker_config,
    build_rabbitmq_consumer,
    build_sa_engine,
    build_sa_sessionmaker,
)
from shop.business_logic.protocols.database_client import DatabaseClientProtocol


def get_container() -> Container:
    container = Container()

    container.add_scoped_by_factory(build_database_config, DatabaseConfig)
    container.add_scoped_by_factory(build_message_broker_config, MessageBrokerConfig)
    container.add_singleton_by_factory(build_sa_engine, AsyncEngine)
    container.add_scoped_by_factory(build_sa_sessionmaker, sessionmaker)
    container.add_scoped_by_factory(build_database_client, DatabaseClientProtocol)
    container.add_scoped_by_factory(build_create_book_service, CreateBookService)
    container.add_scoped_by_factory(build_rabbitmq_consumer, ConsumerProtocol)
    container.add_scoped_by_factory(build_create_order_service, CreateOrderService)

    return container
