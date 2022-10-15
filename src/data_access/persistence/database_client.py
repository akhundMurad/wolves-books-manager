from logging import getLogger
from typing import Any, Callable
from sqlalchemy.ext.asyncio import AsyncSession


logger = getLogger(__name__)


class DatabaseClient:
    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        self._session_factory = session_factory

    async def __aenter__(self) -> "DatabaseClient":
        self._session: AsyncSession = self._session_factory()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            logger.debug(f"Handled exception: {exc_type.__name__} - {exc_val}")
            await self.rollback()
        await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    async def execute(self, statement: str, **params) -> Any:
        return await self._session.execute(statement, params)
