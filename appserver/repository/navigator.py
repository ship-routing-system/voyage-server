import logging
from io import BytesIO
from typing import Dict, Tuple

import numpy as np
from flask_caching import Cache
from voyage import HexGrid
from voyage.navigate import BiDijkstraNavigator, Navigator

from appserver.repository import AvoidZoneRepo
from appserver.commons.exception import RequestError
from appserver.commons.utils import timer
from appserver.config import Config


class NavigatorRepo:
    RESOLUTIONS = {
        "low": (500, 1000),  # (500,  1000) GRID
        "high": (1000, 2000)  # (1000, 2000) GRID
    }
    SIZES = ["all"]
    matrix = None

    def __init__(self, zone_repository:AvoidZoneRepo, cache: Cache, config: Config):
        self.zone_repo = zone_repository
        self.cache = cache
        self.bucket = config.storage_bucket
        self.logger = logging.getLogger(config.LOGGER_NAME)
        self.refresh()

    def get(self, properties: Dict) -> Navigator:
        res = self._parse_resolution(properties)
        size = self._parse_size(properties)
        key = self._resolve_key(res, size)

        matrix = self.cache.get(key)
        if matrix is not None:
            return matrix
        return self._caching(res, key)

    def refresh(self):
        for res in self.RESOLUTIONS.values():
            for size in self.SIZES:
                self._caching(res, size)

    @timer("gunicorn.error")
    def _caching(self, res: Tuple[int, int], size: str) -> Navigator:
        self.logger.info("(%s_%s) 메모리 캐싱을 수행합니다.", res, size)
        cost = self._download_cost(res, size)
        matrix = self.zone_repo.get_matrix(res)
        cost[matrix > 0.] = np.inf
        key = self._resolve_key(res, size)
        self.cache.set(key, cost)

        grid = HexGrid(*cost.shape)
        navigator = BiDijkstraNavigator(cost, grid)
        self.cache.set(key, navigator)
        return navigator

    def _download_cost(self, res: Tuple[int, int], size: str) -> np.ndarray:
        cache_key = self._resolve_key(res, size)
        blob = self.bucket.get_blob(f"navigator/{cache_key}.npy")
        return np.load(BytesIO(blob.download_as_string()))

    def _resolve_key(self, resolution:Tuple[int, int], size:str) -> str:
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
