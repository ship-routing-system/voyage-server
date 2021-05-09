import logging
import pathlib
from io import BytesIO
from typing import Dict

import numpy as np
from flask_caching import Cache
from voyage.grid import HexGrid
from voyage.navigate import Navigator, BiDijkstraNavigator

from appserver.commons.utils import timer
from appserver.config import Config

from appserver.commons.exception import RequestError

ROOT_PATH = pathlib.Path(__file__).parent.absolute()


class NavigatorRepo:
    RESOLUTIONS = {
        "low": "500_1000",  # (500,  1000) GRID
        "high": "1000_2000" # (1000, 2000) GRID
    }

    navigator = None

    def __init__(self, cache: Cache, config: Config):
        self.cache = cache
        self.bucket = config.storage_bucket
        self.logger = logging.getLogger(config.LOGGER_NAME)

    def get(self, properties: Dict) -> Navigator:
        navi_type = self._choose_type(properties)

        navigator = self.cache.get(navi_type)
        if navigator is not None:
            return navigator
        return self._caching(navi_type)

    def _choose_resolution(self, properties: Dict):
        try:
            precision = properties.get("resolution", "low")
            return self.RESOLUTIONS[precision]
        except KeyError:
            raise RequestError("resolution으로는 high와 low 둘 중에서 골라야만합니다.")

    def _choose_size(self, properties: Dict):
        # TODO : Ship Type에 따라 size를 결정짓고 저장
        return "all"

    def _choose_type(self, properties: Dict):
        resolution = self._choose_resolution(properties)
        size = self._choose_size(properties)
        return f"{resolution}_{size}"

    @timer("gunicorn.error")
    def _caching(self, navi_type: str) -> Navigator:
        self.logger.info("%s 메모리 캐싱을 수행합니다.", navi_type)
        cost = self._download_cost(navi_type)
        grid = HexGrid(*cost.shape)
        navigator = BiDijkstraNavigator(cost, grid)
        self.cache.set(navi_type, navigator)
        return navigator

    def _download_cost(self, navi_type: str) -> np.ndarray:
        blob_path = f"navigator/{navi_type}.npy"
        blob = self.bucket.get_blob(blob_path)
        return np.load(BytesIO(blob.download_as_string()))
