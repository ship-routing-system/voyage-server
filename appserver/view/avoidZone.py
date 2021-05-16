from json.decoder import JSONDecodeError

import flask
import geojson
from flask import request
from geojson import Feature, MultiPolygon, Polygon

from appserver.commons import RequestError
from appserver.service import AvoidZoneService


def create_avoid_zone_endpoints(app: flask.Flask, service: AvoidZoneService):
    @app.route("/avoid-zone", methods=['GET'])
    def find_all_avoid_zone():
        if 'id' in request.args:
            return service.find(request.args['id']), 200
        return service.find_all(), 200

    @app.route("/avoid-zone", methods=['POST'])
    def save_avoid_zone():
        service.save(parse_inputs(request.data))
        return "success", 200

    @app.route("/avoid-zone", methods=['DELETE'])
    def delete_avoid_zone():
        if 'id' not in request.args:
            raise RequestError("query에 id를 지정해주어야 합니다.")
        service.delete(request.args['id'])
        return "success", 200

    def parse_inputs(string) -> Feature:
        try:
            inputs = geojson.loads(string)
        except JSONDecodeError as error:
            raise RequestError("request body는 json으로 이루어져야 합니다.")

        if not isinstance(inputs, Feature):
            raise RequestError("request body는 Feature type이어야 합니다.")

        polygons = inputs["geometry"]

        if not (isinstance(polygons, MultiPolygon) or isinstance(polygons, Polygon)):
            raise RequestError("request geometry는 MultiPolygon, Polygon Type이어야 합니다.")

        if "id" not in inputs:
            raise RequestError("request는 id가 필수적으로 지정되어야 합니다")

        if not inputs.is_valid:
            raise RequestError("유효한 geojson 형식이 아닙니다.")

        return inputs
