from typing import List, Tuple, Dict

from geojson import MultiPoint, LineString, Feature

from appserver.commons.utils import timer
from appserver.repository import NavigatorRepo
from appserver.service.navigation.optimization import PathOptimizer
from appserver.service.navigation.utils import extract_points, calculate_distance, merge_path, carry_on


class Navigator:
    def __init__(self, repository: NavigatorRepo, optimizer: PathOptimizer):
        self.repository = repository
        self.optimizer = optimizer

    def navigate(self, inputs: MultiPoint, properties: Dict) -> Feature:
        # navigator 모형을 가져오기
        navigator = self.repository.get(properties)

        # geojson으로부터 좌표 정보 추출하기
        pts = extract_points(inputs)

        # 각 구간 별 경로 탐색하기
        intervals = [self._navigate_interval(pts[i], pts[i + 1], navigator)
                     for i in range(len(pts) - 1)]

        # 경로를 병합하기
        path = merge_path(intervals)

        # geojson 타입으로 반환하기
        return Feature(
            geometry=LineString(path, precision=3),
            properties={"distance": calculate_distance(path)}
        )

    @timer("gunicorn.error")
    def _navigate_interval(self, start, end, navigator) -> List[Tuple]:
        # 구간에 대한 경로 탐색하기
        path = navigator.navigate(start, end)
        # 경로 결과를 정형화하기
        coordinates = carry_on(path)
        # 칼만 필터를 통해 정형화하기
        return self.optimizer.optimize(coordinates)
