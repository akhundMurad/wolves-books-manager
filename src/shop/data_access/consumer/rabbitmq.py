import json
import logging
from uuid import UUID
from aio_pika import ExchangeType, IncomingMessage, connect

from shop.business_logic.books.service.create_book_service import CreateBookService


class Consumer:
    def __init__(self, connection_string: str, service: CreateBookService) -> None:
        self._connection_string = connection_string
        self._service = service

    async def consume(self) -> None:
        connection = await connect(self._connection_string)
        channel = await connection.channel()
        exchange = await channel.declare_exchange("books", ExchangeType.FANOUT)
        queue = await channel.declare_queue("books")

        await queue.bind(exchange, "books")

        async with connection:
            async with queue.iterator() as qiterator:
                async for message in qiterator:
                    await self.process_message(message)

    async def process_message(self, message: IncomingMessage) -> None:
        async with message.process(requeue=True):
            body = message.body
            payload = json.loads(body)

            logging.info(f"Recieved message {message.message_id} from rabbitmq.")
            await self._service.execute(
                id=UUID(payload.get("id")),
                title=payload.get("title"),
                description=payload.get("description"),
                author_full_name=payload.get("author_full_name"),
                genre=payload.get("genre"),
                price=float(payload.get("price")),
            )
