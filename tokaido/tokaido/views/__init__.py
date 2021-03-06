import logging
import http
from typing import (
    Dict,
    List,
    Set,
)

import colander
import pyramid.request
import pyramid.response
import pyramid.view

import tokaido.domain
import tokaido.exceptions
import tokaido.models


logger = logging.getLogger(__name__)


@pyramid.view.view_config(context=Exception)
def handle_error(error: Exception, request: pyramid.request.Request) -> pyramid.response.Response:
    logging.info("Some error is propagated to view layer.")

    url, params, body = request.url, request.params, request.text

    try:
        raise error
    except tokaido.exceptions.ResourceNotFoundError:
        return pyramid.response.Response(status=http.HTTPStatus.NOT_FOUND)
    except:
        logger.exception("Unexpected Error. URL: %s, Body: %s, Params", url, body, params)
        return pyramid.response.Response(status=http.HTTPStatus.INTERNAL_SERVER_ERROR)


@pyramid.view.view_config(route_name='index', renderer="templates/index.jinja2")
def index(request: pyramid.request.Request) -> Dict[str, List[tokaido.models.Step]]:
    return {
        'steps': tokaido.domain.Step.all(),
    }


@pyramid.view.view_config(route_name='api_create_step', renderer='json')
def api_add_step(request: pyramid.request.Request) -> pyramid.response.Response:
    class Schema(colander.MappingSchema):
        title = colander.SchemaNode(colander.String())

    request.response.status = http.HTTPStatus.CREATED
    return tokaido.domain.Step.create(**Schema().deserialize(request.json_body))


class IntegerSet:
    def __init__(self) -> None:
        self.colander_set = colander.Set()

    def serialize(self, node, appstruct):
        return self.colander_set.serialize(node, appstruct)

    def deserialize(self, node, cstruct) -> Set[int]:
        return set(int(element) for element in self.colander_set.deserialize(node, cstruct))


@pyramid.view.view_config(route_name='api_update_step', renderer='json')
def api_update_step(request: pyramid.request.Request) -> pyramid.response.Response:
    class Schema(colander.MappingSchema):
        id = colander.SchemaNode(colander.Integer())
        title = colander.SchemaNode(colander.String())
        next_step_ids = colander.SchemaNode(IntegerSet())

    request.response.status = http.HTTPStatus.OK
    return tokaido.domain.Step.update(
        **Schema().deserialize(
            dict(id=request.matchdict['step_id'], **request.json_body)
        )
    )


@pyramid.view.view_config(route_name='api_get_step', renderer='json')
def api_get_step(request: pyramid.request.Request) -> pyramid.response.Response:
    class Schema(colander.MappingSchema):
        id = colander.SchemaNode(colander.Integer())

    request.response.status = http.HTTPStatus.OK
    return tokaido.domain.Step.get(
        **Schema().deserialize(
            {
                'id': request.matchdict['step_id']
            }
        )
    )
