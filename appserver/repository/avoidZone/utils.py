from typing import Tuple

import cv2
import numpy as np
from shapely.coords import CoordinateSequence
from shapely.geometry import Polygon, MultiPolygon


def polygon2matrix(polygon: MultiPolygon, im_size: Tuple[int, int]) -> np.ndarray:
    if isinstance(polygon, Polygon):
        polygons = MultiPolygon(polygons=[polygon])
    else:
        polygons = polygon

    img_mask = np.zeros(im_size, np.uint8)
    exteriors = [adjust_coord(poly.exterior.coords, im_size) for poly in polygons]
    interiors = [adjust_coord(pi.coords, im_size)
                 for poly in polygons for pi in poly.interiors]
    cv2.fillPoly(img_mask, exteriors, 1)
    cv2.fillPoly(img_mask, interiors, 0)
    return img_mask


def adjust_coord(coords: CoordinateSequence, im_size: Tuple[int, int]):
    shift = np.array(coords) + np.array([180, -90])
    scale = shift * np.array([1 / 360, -1 / 180]) * np.array(im_size)[::-1]
    return scale.round().astype(np.int32)
