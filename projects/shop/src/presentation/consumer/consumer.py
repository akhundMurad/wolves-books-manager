import asyncio
import logging

from src.di.container import get_container
from src.business_logic.protocols.consumer import ConsumerProtocol


async def consume() -> None:
    logging.basicConfig(level=logging.INFO)

    container = get_container()
    provider = container.build_provider()

    consumer = provider.get(ConsumerProtocol)

    logging.info("Starting to consume messages...")
    await consumer.consume()


if __name__ == "__main__":
    asyncio.run(consume())
