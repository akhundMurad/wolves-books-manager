from blacksheep import Application


def build_asgi():
    app = Application()

    return app


asgi = build_asgi()
