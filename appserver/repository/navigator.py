import pathlib
from io import BytesIO
from typing import Dict

import numpy as np
from flask_caching import Cache
from voyage.grid import HexGrid
from voyage.navigate import Navigator, BiDijkstraNavigator

from appserver.config import Config

ROOT_PATH = pathlib.Path(__file__).parent.absolute()


class NavigatorRepo:
    navigator = None

    def __init__(self, cache: Cache, config: Config):
        self.cache = cache
        self.bucket = config.storage_bucket

    def get(self, properties: Dict) -> Navigator:
        navi_type = self._choose_type(properties)

        navigator = self.cache.get(navi_type)
        if navigator is not None:
            return navigator
        return self._caching(navi_type)

    def _choose_type(self, properties: Dict):
        if "imo_no" in properties:
            pass
        return "default"

    def _caching(self, navi_type: str) -> Navigator:
        cost = self._download_cost(navi_type)
        grid = HexGrid(*cost.shape)
        navigator = BiDijkstraNavigator(cost, grid)
        self.cache.set(navi_type, navigator)
        return navigator

    def _download_cost(self, navi_type: str) -> np.ndarray:
        blob_path = f"navigator/{navi_type}.npy"
        blob = self.bucket.get_blob(blob_path)
        return np.load(BytesIO(blob.download_as_string()))
