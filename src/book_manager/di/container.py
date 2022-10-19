from rodi import Container
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from src.business_logic.create_book_service import CreateBookService

from src.config import DatabaseConfig, JWTConfig
from src.di.factories import (
    build_create_book_service,
    build_database_client,
    build_database_config,
    build_jwt_config,
    build_jwt_manager,
    build_sa_engine,
    build_sa_sessionmaker,
)
from src.business_logic.protocols.database_client import DatabaseClientProtocol
from src.presentation.api.auth import JWTManager


def get_container() -> Container:
    container = Container()

    container.add_scoped_by_factory(build_database_config, DatabaseConfig)
    container.add_scoped_by_factory(build_jwt_config, JWTConfig)
    container.add_singleton_by_factory(build_sa_engine, AsyncEngine)
    container.add_scoped_by_factory(build_sa_sessionmaker, sessionmaker)
    container.add_scoped_by_factory(build_database_client, DatabaseClientProtocol)
    container.add_scoped_by_factory(build_create_book_service, CreateBookService)
    container.add_scoped_by_factory(build_jwt_manager, JWTManager)

    return container
