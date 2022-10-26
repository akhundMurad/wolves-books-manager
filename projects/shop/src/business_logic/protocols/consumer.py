from typing import Protocol


class ConsumerProtocol(Protocol):
    async def consume(self) -> None:
        ...
