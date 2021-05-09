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

ROOT_PATH = pathlib.Path(__file__).parent.absolute()


class NavigatorRepo:
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

    def _choose_type(self, properties: Dict):
        if "imo_no" in properties:
            return "1000_2000_all"
        return "default"

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
