import asyncio
import logging
from tenacity import retry
from tenacity.stop import stop_after_attempt

from src.di.container import get_container
from src.business_logic.protocols.consumer import ConsumerProtocol


@retry(stop=stop_after_attempt(3))
async def consume() -> None:
    logging.basicConfig(level=logging.INFO)

    container = get_container()
    provider = container.build_provider()

    consumer = provider.get(ConsumerProtocol)

    logging.info("Starting to consume messages...")
    await consumer.consume()


if __name__ == "__main__":
    asyncio.run(consume())
