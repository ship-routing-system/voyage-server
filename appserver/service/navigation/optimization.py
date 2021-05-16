from typing import List, Tuple

from voyage.utils import KalmanFilter

from appserver.commons.utils import timer


class PathOptimizer:
    def __init__(self, kalman: KalmanFilter):
        self.kalman = kalman

    @timer("gunicorn.error")
    def optimize(self, path: List[Tuple]) -> List:
        self.kalman.reset()
        return [self.kalman.estimate(lat, lon).tolist()[::-1] for lat, lon in path]
