import logging
import os
from typing import Dict

import geojson
from flask_caching import Cache
from shapely.geometry import shape, MultiPolygon

from appserver.commons.exception import ServerError
from appserver.config import Config


class AvoidZoneRepo:
    PREFIX = "avoid-zone"

    def __init__(self, cache: Cache, config: Config):
        self.cache = cache
        self.bucket = config.storage_bucket
        self.logger = logging.getLogger(config.LOGGER_NAME)

    def get(self) -> Dict[str, MultiPolygon]:
        avoid_zone = self.cache.get(self.PREFIX)
        if avoid_zone is not None:
            return avoid_zone
        return self._caching()

    def _caching(self):

        avoid_zone = {}
        try:
            for blob in self.bucket.list_blobs(prefix=self.PREFIX):
                name = os.path.splitext(blob.name[len(self.PREFIX):].split("/")[1])[0]
                if name:
                    zone = geojson.loads(blob.download_as_string())
                    avoid_zone[name] = shape(zone)
        except Exception as e:
            raise ServerError("avoid-zone 세팅에 문제가 발생했습니다.")
        self.cache.set(self.PREFIX, avoid_zone)
        return avoid_zone
