from json.decoder import JSONDecodeError
from typing import Tuple, Dict

import flask
import geojson
from flask import request, jsonify
from geojson import Feature, MultiPoint

from appserver.commons import RequestError
from appserver.service import Navigator, AvoidZoneValidator


def create_navigation_endpoints(app: flask.Flask, validator: AvoidZoneValidator, navigator: Navigator):
    @app.route("/navigation", methods=['GET', 'POST'])
    def navigate():
        inputs, properties = parse_inputs(request.data)
        validator.validate(inputs)
        outputs = navigator.navigate(inputs, properties)
        return jsonify(outputs), 200

    def parse_inputs(string) -> Tuple[MultiPoint, Dict]:
        try:
            inputs = geojson.loads(string)
        except JSONDecodeError as error:
            raise RequestError("request body는 json으로 이루어져야 합니다.") from error

        if not isinstance(inputs, Feature):
            raise RequestError("request body는 Feature type이어야 합니다.")

        points = inputs["geometry"]

        if not isinstance(points, MultiPoint):
            raise RequestError("request geometry는 MultiPoint Type이어야 합니다.")

        properties = inputs['properties']
        return points, properties
