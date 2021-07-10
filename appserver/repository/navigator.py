import logging
from io import BytesIO
from typing import Dict, Tuple

import numpy as np
from flask_caching import Cache
from voyage.navigate import Navigator, FastNavigator

from appserver.commons.exception import RequestError
from appserver.commons.utils import timer
from appserver.config import Config
from appserver.repository import AvoidZoneRepo


class NavigatorRepo:
    RESOLUTIONS = {
        "low": (500, 1000),  # (500,  1000) GRID
        "high": (1000, 2000)  # (1000, 2000) GRID
    }
    SIZES = ["all"]
    matrix = None

    def __init__(self, zone_repository: AvoidZoneRepo, cache: Cache, config: Config):
        self.zone_repo = zone_repository
        self.cache = cache
        self.bucket = config.storage_bucket
        self.logger = logging.getLogger(config.LOGGER_NAME)
        self.refresh()

    def get(self, properties: Dict) -> Navigator:
        resolution = self._parse_resolution(properties)
        size = self._parse_size(properties)
        key = self._resolve_key(resolution, size)

        matrix = self.cache.get(key)
        if matrix is not None:
            return matrix
        return self._caching(key, resolution)

    def refresh(self):
        for resolution in self.RESOLUTIONS.values():
            for size in self.SIZES:
                key = self._resolve_key(resolution, size)
                self._caching(key, resolution)

    @timer("gunicorn.error")
    def _caching(self, key: str, resolution: Tuple) -> Navigator:
        self.logger.info("(key) 메모리 캐싱을 수행합니다.", key)
        cost = self._download_cost(key)
        matrix = self.zone_repo.get_matrix(resolution)
        cost[matrix > 0.] = np.inf
        self.cache.set(key, cost)

        navigator = FastNavigator(cost)
        self.cache.set(key, navigator)
        return navigator

    def _download_cost(self, key: str) -> np.ndarray:
        blob = self.bucket.get_blob(f"navigator/{key}.npy")
        return np.load(BytesIO(blob.download_as_string()))

    def _resolve_key(self, resolution: Tuple[int, int], size: str) -> str:
        return f"{resolution[0]}_{resolution[1]}_{size}"

    def _parse_resolution(self, properties: Dict) -> Tuple[int, int]:
        try:
            precision = properties.get("resolution", "low")
            return self.RESOLUTIONS[precision]
        except KeyError:
            raise RequestError("resolution으로는 high와 low 둘 중에서 골라야만합니다.")

    def _parse_size(self, properties: Dict):
        # TODO : Ship Type에 따라 size를 결정짓고 저장
        return "all"
