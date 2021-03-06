from flask import Flask
from flask_caching import Cache
from voyage.utils import KalmanFilter

from appserver.config import Config, DevConfig
from appserver.repository import AvoidZoneRepo, NavigatorRepo
from appserver.service import Navigator, PathOptimizer, AvoidZoneValidator, AvoidZoneService
from appserver.view import create_navigation_endpoints, create_exception_handler, create_avoid_zone_endpoints


def create_app(cfg: Config):
    app = Flask(__name__)
    app.config.from_mapping(vars(cfg))
    cache = Cache(app)

    ## Create Persistenace Layer
    avoidzone_repository = AvoidZoneRepo(cache, cfg)
    navigator_repository = NavigatorRepo(avoidzone_repository, cache, cfg)

    ## Create Business Layer
    kalman_filter = KalmanFilter(cfg.SYSTEM_NOISE, cfg.SENSOR_NOISE, cfg.INIT_NOISE)
    path_optimizer = PathOptimizer(kalman_filter)
    navigator = Navigator(navigator_repository, path_optimizer)

    zone_validator = AvoidZoneValidator(avoidzone_repository)
    zone_service = AvoidZoneService(cache, avoidzone_repository)

    ## Create Endpoint
    create_navigation_endpoints(app, zone_validator, navigator)
    create_avoid_zone_endpoints(app, zone_service)
    create_exception_handler(app)

    return app


if __name__ == "__main__":
    config = DevConfig()
    app = create_app(config)
    app.run(host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG)
