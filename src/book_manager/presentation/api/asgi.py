from blacksheep import Application
from blacksheep.server.openapi.v3 import OpenAPIHandler
from guardpost import Policy
from guardpost.common import AuthenticatedRequirement
from openapidocs.v3 import Info
from book_manager.presentation.api.auth import JWTAuthHandler

from book_manager.presentation.api.controllers import Books  # noqa
from book_manager.di.container import get_container


def build_application() -> Application:
    app = Application()
    open_api = OpenAPIHandler(info=Info("Books app API", version="0.0.1"))
    open_api.bind_app(app)
    container = get_container()
    provider = container.build_provider()

    app.services = container

    app.use_authentication().add(JWTAuthHandler(provider))
    app.use_authorization().add(Policy("authenticated", AuthenticatedRequirement()))

    return app


asgi = build_application()
