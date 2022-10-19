from blacksheep import FromJSON, Response
from blacksheep.server.controllers import APIController, post

from shop.business_logic.orders.commands.create_order_command import CreateOrderCommand
from shop.business_logic.orders.service.create_order_service import CreateOrderService


class Orders(APIController):
    @post("/")
    async def create_book(
        self, command: FromJSON[CreateOrderCommand], service: CreateOrderService
    ) -> Response:
        await service.execute(command=command.value)

        return Response(status=201)
