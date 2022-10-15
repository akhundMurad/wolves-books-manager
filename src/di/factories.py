from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from rodi import GetServiceContext

from src.business_logic.create_book_service import CreateBookService
from src.business_logic.protocols.database_client import DatabaseClientProtocol
from src.config import DatabaseConfig, JWTConfig
from src.data_access.persistence.database_client import DatabaseClient
from src.presentation.api.auth import JWTManager


def build_database_config(context: GetServiceContext) -> DatabaseConfig:
    return DatabaseConfig()


def build_jwt_config(context: GetServiceContext) -> JWTConfig:
    return JWTConfig()


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
    database_client: DatabaseClient = context.provider[DatabaseClientProtocol]
    return CreateBookService(database_client=database_client)


def build_jwt_manager(context: GetServiceContext) -> JWTManager:
    config: JWTConfig = context.provider[JWTConfig]

    return JWTManager(key=config.JWT_KEY, algorithm=config.JWT_ALGORITHM)
