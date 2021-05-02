import itertools
from typing import List, Tuple

import geojson
from geojson import MultiPoint
from voyage.grid import Cell
from voyage.utils.distance import haversine


def merge_path(paths: List[List[Tuple]]) -> List[Tuple]:
    """
    이어진 경로를 병합
    [[(a1,a2),(b1,b2),(c1,c2)],[(d1,d2),(e1,e2)],[(f1,f2)]]
    -> [(a1,a2),(b1,b2),(c1,c2), (d1,d2),(e1,e2), (f1,f2)]

    Args:
        paths: 경로들의 리스트

    Returns: List[Tuple]
        병합된 리스트
    """
    return list(itertools.chain(*paths))


def calculate_distance(path: List[Tuple]) -> float:
    """
    경로의 총 길이를 계산, 경로 내 포인트 간의 거리를 더하는 방식
    Args:
        path: 경로

    Returns:

    """
    return sum(haversine(path[i], path[i + 1])
               for i in range(len(path) - 1))


def extract_points(coordinates: MultiPoint) -> List[Tuple]:
    """
    주어진 geojson으로부터 좌표정보(위경도 정보)를 추출
    * 위도: -90. ~ 90.
    * 경도 : -180. ~ 180.
    범위를 가지도록 보정하는 작업도 수행

    Args:
        path: 경로

    Returns:

    """

    def adjust(point):
        lon, lat = point
        while lat < -90 or lat > 90:
            if lat < -90:
                lat += 180
            else:
                lat -= 180

        while lon < -180 or lon > 180:
            if lon < -180:
                lon += 360
            else:
                lon -= 360
        return lat, lon

    return [adjust(point) for point in geojson.utils.coords(coordinates)]


def carry_on(path: List[Cell]) -> List[Tuple]:
    """
    경도는 -180도에서 조금만 더 가면 바로 180도로 넘어가는 등, 지구가 둥글기 때문에 발생하는 이슈가 존재. 이를 이어주는 로직이 필요

    Args:
        path:

    Returns:

    """
    if len(path) == 0:
        return []

    def on_the_border(prev, curr):
        sign = prev * curr < 0
        size = abs(prev) + abs(curr) > 180
        return sign and size

    start = path[0].lat, path[0].lon
    res = [start]
    for cell in path[1:]:
        prev_lon = res[-1][1]
        curr_lat, curr_lon = cell.lat, cell.lon
        if on_the_border(prev_lon, curr_lon):
            curr_lon += 360 if curr_lon < 0 else -360
        res.append((curr_lat, curr_lon))
    return res
