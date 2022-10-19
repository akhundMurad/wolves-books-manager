from typing import Any, Protocol


class DatabaseClientProtocol(Protocol):
    async def __aenter__(self) -> "DatabaseClientProtocol":
        ...

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        ...

    async def commit(self) -> None:
        ...

    async def rollback(self) -> None:
        ...

    async def execute(self, statement: str, **params) -> Any:
        ...
