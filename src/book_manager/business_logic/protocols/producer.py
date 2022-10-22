from typing import Protocol


class ProducerProtocol(Protocol):
    async def publish(self, *, message: dict, exchange_name: str) -> None:
        ...
