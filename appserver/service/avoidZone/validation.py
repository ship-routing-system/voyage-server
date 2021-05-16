import geojson
from shapely.geometry import Point

from appserver.commons import RequestError
from appserver.repository import AvoidZoneRepo


class AvoidZoneValidator:
    def __init__(self, repository: AvoidZoneRepo):
        self.repository = repository

    def validate(self, inputs: geojson.MultiPoint):
        avoid_zones = self.repository.get()

        for zone_name, zone in avoid_zones.items():
            for coord in geojson.utils.coords(inputs):
                point = Point(*coord)
                if zone.contains(point):
                    raise RequestError(f"좌표({coord})가 avoid zone({zone_name}) 위에 존재합니다.")
