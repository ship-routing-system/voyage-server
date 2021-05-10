from flask import Flask
from flask_caching import Cache
from voyage.utils import KalmanFilter

from appserver.config import Config, DevConfig
from appserver.repository import NavigatorRepo, AvoidZoneRepo
from appserver.service import Navigator, PathOptimizer, AvoidZoneValidator
from appserver.view import create_navigation_endpoints, create_exception_handler


def create_app(cfg: Config):
    app = Flask(__name__)
    app.config.from_mapping(vars(cfg))
    cache = Cache(app)

    ## Create Persistenace Layer
    navigator_repository = NavigatorRepo(cache, cfg)
    avoidzone_repository = AvoidZoneRepo(cache, cfg)

    ## Create Business Layer
    kalman_filter = KalmanFilter(cfg.SYSTEM_NOISE, cfg.SENSOR_NOISE, cfg.INIT_NOISE)
    path_optimizer = PathOptimizer(kalman_filter)
    navigator = Navigator(navigator_repository, path_optimizer)

    zone_validator = AvoidZoneValidator(avoidzone_repository)

    ## Create Endpoint
    create_navigation_endpoints(app, zone_validator, navigator)
    create_exception_handler(app)

    return app


if __name__ == "__main__":
    config = DevConfig()
    app = create_app(config)
    app.run(host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG)
