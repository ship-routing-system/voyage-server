import flask
from flask import jsonify

from appserver.commons import BaseError, RequestError


def create_exception_handler(app: flask.Flask):
    @app.errorhandler(BaseError)
    def handle(error: BaseError):
        response = {
            "success": False,
            "error": {
                "type": error.__class__.__name__,
                "message": error.msg
            }
        }
        return jsonify(response), error.status_code

    @app.errorhandler(404)
    def handle_404(error: BaseError):
        return jsonify({
            "success": False,
            "error": {
                "type": RequestError.__name__,
                "message": "잘못된 URL입니다."
            }
        }), 400
