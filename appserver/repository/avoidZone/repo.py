import logging
import os
from typing import Dict

import geojson
import numpy as np
from flask_caching import Cache
from geojson import Feature
from google.api_core.exceptions import NotFound
from shapely.geometry import shape, MultiPolygon

from appserver.commons.exception import ServerError
from appserver.config import Config
from .utils import polygon2matrix


class AvoidZoneRepo:
    PREFIX = "avoid-zone"

    def __init__(self, cache: Cache, config: Config):
        self.cache = cache
        self.bucket = config.storage_bucket
        self.logger = logging.getLogger(config.LOGGER_NAME)
        self.refresh()

    def get(self) -> Dict[str, MultiPolygon]:
        avoid_zone = self.cache.get(self.PREFIX)
        if avoid_zone is not None:
            return avoid_zone
        return self.refresh()

    def get_matrix(self, im_size) -> np.ndarray:
        result = [polygon2matrix(polygon, im_size) for key, polygon in self.get().items() if key != "ground"]
        if result:
            return np.stack(result).sum(axis=0)
        return np.zeros(im_size)

    def save(self, id: str, feature: Feature):
        blob = self.bucket.blob(f"{self.PREFIX}/{id}.geojson")
        blob.upload_from_string(data=geojson.dumps(feature), content_type="application/json")

    def delete(self, id: str):
        try:
            self.bucket.delete_blob(f"{self.PREFIX}/{id}.geojson")
        except NotFound:
            raise ServerError(f"존재하지 않은 id({id})입니다.")

    def refresh(self):
        avoid_zone = {}
        try:
            for blob in self.bucket.list_blobs(prefix=self.PREFIX):
                name = os.path.splitext(blob.name[len(self.PREFIX):].split("/")[1])[0]
                if name:
                    zone = geojson.loads(blob.download_as_string())
                    avoid_zone[name] = shape(zone['geometry'])
        except Exception as e:
            raise ServerError("avoid-zone 세팅에 문제가 발생했습니다.")
        self.cache.set(self.PREFIX, avoid_zone)
        return avoid_zone
