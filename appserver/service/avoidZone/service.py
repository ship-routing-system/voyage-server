from flask_caching import Cache
from geojson import Feature, FeatureCollection
from shapely.geometry import mapping

from appserver.repository import AvoidZoneRepo


class AvoidZoneService:
    def __init__(self, cache: Cache, repo: AvoidZoneRepo):
        self.cache = cache
        self.repo = repo

    def find_all(self) -> FeatureCollection:
        return FeatureCollection([Feature(id=key, geometry=mapping(value)) for key, value in self.repo.get().items()])

    def save(self, feature: Feature):
        self.repo.save(feature["id"], feature)
        self.cache.clear()

    def delete(self, id: str):
        self.repo.delete(id)
        self.cache.clear()
