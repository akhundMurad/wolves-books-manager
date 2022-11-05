from blacksheep import Application
from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Info
from src.di.container import get_container

from src.presentation.api.controllers import Orders  # noqa


def build_asgi():
    app = Application()
    open_api = OpenAPIHandler(info=Info("Books app API", version="0.0.1"))
    open_api.bind_app(app)
    container = get_container()
    app.services = container

    return app


asgi = build_asgi()
