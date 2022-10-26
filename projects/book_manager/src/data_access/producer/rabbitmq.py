import json
import logging
from aio_pika import ExchangeType, Message, connect


class Producer:
    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string

    async def publish(self, *, message: dict, exchange_name: str) -> None:
        connection = await connect(self._connection_string)
        async with connection:
            channel = await connection.channel()

            exchange = await channel.declare_exchange(
                exchange_name, ExchangeType.FANOUT
            )

            rq_message = Message(json.dumps(message, default=str).encode("utf-8"))

            await exchange.publish(rq_message, routing_key="books")
            logging.debug(f"Sent message {rq_message.message_id} to RabbitMQ.")
