from typing import Type
import pytest
from rodi import Container

from book_manager.business_logic.protocols.database_client import DatabaseClientProtocol
from book_manager.data_access.persistence.database_client import DatabaseClient
from book_manager.di.container import get_container
from book_manager.config import DatabaseConfig


@pytest.fixture
def book_data() -> dict:
    return {
        "title": "Title",
        "description": "Description",
        "price": 100.20,
        "genre": "Fantasy",
        "author_full_name": "Full Name",
    }


@pytest.fixture
def test_database_config() -> Type:
    return type(
        "TestDatabaseConfig",
        (),
        {
            "DATABASE_URL": "postgresql+asyncpg://postgres:somepassword@localhost:5432/books_test"
        },
    )


@pytest.fixture(scope="session")
def test_container(test_database_config) -> Container:
    container = get_container()
    container.add_scoped_by_factory(
        lambda context: test_database_config(), DatabaseConfig
    )


@pytest.fixture
def database_client(test_container: Container) -> DatabaseClientProtocol:
    provider = test_container.build_provider()
    return provider.get(DatabaseClientProtocol)
