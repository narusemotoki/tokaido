import logging
import http
from typing import (
    Dict,
    List,
)

import pyramid.request
import pyramid.response
import pyramid.view

import tokaido.domain
import tokaido.models


logger = logging.getLogger(__name__)


@pyramid.view.view_config(context=Exception)
def handle_error(error: Exception, request: pyramid.request.Request) -> pyramid.response.Response:
    logging.info("Some error is propagated to view layer.")

    url, params, body = request.url, request.params, request.text

    try:
        raise error
    except:
        logger.exception("Unexpected Error. URL: %s, Body: %s, Params", url, body, params)
        return pyramid.response.Response(status=http.HTTPStatus.INTERNAL_SERVER_ERROR)


@pyramid.view.view_config(route_name='index', renderer="templates/index.jinja2")
def index(request: pyramid.request.Request) -> Dict[str, List[tokaido.models.Step]]:
    return {
        'steps': tokaido.domain.index()
    }
