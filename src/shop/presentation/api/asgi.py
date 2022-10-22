from blacksheep import Application
from shop.di.container import get_container


def build_asgi():
    app = Application()
    container = get_container()
    app.services = container

    return app


asgi = build_asgi()
