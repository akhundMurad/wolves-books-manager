from uuid import uuid4

from src.business_logic.exceptions import BusinessLogicException
from src.business_logic.orders.commands.create_order_command import CreateOrderCommand
from src.business_logic.protocols.database_client import DatabaseClientProtocol
from src.data_access.persistence.tables import books, ordered_books, orders


class CreateOrderService:
    def __init__(self, database_client: DatabaseClientProtocol) -> None:
        self._db = database_client

    async def execute(self, *, command: CreateOrderCommand) -> None:
        async with self._db:
            await self.check_books_existence(command=command)
            # await self.check_customer_existence(command=command)

            external_id = uuid4()
            statement = f"""
            INSERT INTO {orders.name}(external_id, customer) 
            VALUES(:external_id, :customer)
            """
            await self._db.execute(
                statement, external_id=external_id, customer=command.customer
            )

            values = []
            for ordered_book in command.books:
                values.append(
                    f"({str(ordered_book.book_id)}, {str(external_id)}, {str(ordered_book.quantity)}),"
                )

            statement = f"""
            INSERT INTO {ordered_books.name}(book_id, order_id, quantity)
            VALUES
                {" ".join(values)[::-1]}
            """
            await self._db.execute(statement)

            await self._db.commit()

    async def check_books_existence(self, *, command: CreateOrderCommand) -> None:
        book_ids = [str(ordered_book.book_id) for ordered_book in command.books]
        book_ids_statement = ", ".join(book_ids)
        statement = f"""
        SELECT external_id, quantity 
        FROM {books.name} WHERE external_id IN ({book_ids_statement})
        """

        records = await self._db.execute(statement)

        exc_messages = []
        for ordered_book in command.books:
            record = list(
                filter(
                    lambda record: record["external_id"] == ordered_book.book_id,
                    records,
                )
            )
            if not record or ordered_book.quantity > record[1]:
                exc_messages.append(f"There is no book with id {ordered_book.book_id}.")

        if exc_messages:
            raise BusinessLogicException(exc_messages)

    # async def check_customer_existence(self, *, command: CreateOrderCommand) -> None:
    #     statement = f"""
    #     SELECT id FROM customers WHERE external_id = :customer
    #     """

    #     records = await self._db.execute(statement, customer=command.customer)
    #     if not records:
    #         raise BusinessLogicException("Customer with this ID was not found.")
