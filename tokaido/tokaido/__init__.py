import logging
from typing import (
    Any,
    Dict,
)

import pyramid.config
import pyramid.renderers
import pyramid.router
import sqlalchemy
import sqlalchemy.exc
import sqlalchemy.pool


import tokaido.config
import tokaido.models


def init_logging() -> None:
    logging.basicConfig(
        format="%(asctime)s %(levelname)-5.5s [%(name)s:%(lineno)s][%(threadName)s] %(message)s",
        level=tokaido.config.LOG_LEVEL
    )


def init_database() -> None:
    engine = sqlalchemy.create_engine(
        tokaido.config.DATA_SOURCE_NAME,
        echo=tokaido.config.LOG_LEVEL <= logging.DEBUG,
    )
    tokaido.models.DBSession.configure(bind=engine)
    tokaido.models.Base.metadata.bind = engine
    tokaido.models.Base.metadata.create_all(bind=engine)


def init_json_renderer(config: pyramid.config.Configurator) -> None:
    renderer = pyramid.renderers.JSON()

    def step_adapter(
            step: tokaido.models.Step, request: pyramid.request.Request) -> Dict[str, Any]:
        return {
            'id': step.id,
            'title': step.title,
        }

    renderer.add_adapter(tokaido.models.Step, step_adapter)
    config.add_renderer('json', renderer)


def init_wsgi_app() -> pyramid.router.Router:
    config = pyramid.config.Configurator(settings={
        'pyramid.includes': [
            'pyramid_jinja2',
            'pyramid_tm',
        ],
        'pyramid.reload_templates': True,
    })

    for name, path, method in [
            ('index', "/", 'GET'),
            ('api_create_step', "/api/steps", 'POST'),
            ('api_update_step', "/api/steps/{step_id:\d+}", 'PUT'),
    ]:
        config.add_route(name, path, request_method=method)
    config.scan()

    return config.make_wsgi_app()


def main(*args, **kwargs) -> pyramid.router.Router:
    init_logging()
    init_database()

    return init_wsgi_app()
