import numpy as np

from . import Cell, Grid


class HexCell(Cell):
    NEIGHBOR_ODD_OFFSETS = ((-1, -1), (-1, 0), (0, 1), (1, 0), (1, -1), (0, -1))
    NEIGHBOR_EVEN_OFFSETS = ((-1,  0), (-1, 1), (0, 1), (1, 1), (1, 0), (0, -1))

    def __init__(self, lat_index: int, lon_index: int, matrix: Grid):
        self.lat_index = lat_index
        self.lon_index = lon_index
        self.matrix = matrix

    def neighbors(self):
        """ 해당 Cell의 neighbor cell 집합을 반환
        :return:
        """
        result = set()
        neighbor_offsets = self.NEIGHBOR_ODD_OFFSETS if self.lat_index % 2 else self.NEIGHBOR_EVEN_OFFSETS

        len_lat, len_lon = self.matrix.shape
        for lat_offset, lon_offset in neighbor_offsets:
            res_lat_index = self.lat_index + lat_offset
            res_lon_index = self.lon_index + lon_offset

            if res_lat_index < 0 or res_lat_index >= len_lat:
                continue

            if res_lon_index < 0:
                res_lon_index = len_lon + res_lon_index
            elif res_lon_index >= len_lon:
                res_lon_index = res_lon_index - len_lon

            result.add(HexCell(res_lat_index, res_lon_index, self.matrix))

        return result

    @property
    def lat(self):
        return self.matrix.lat_offset - self.matrix.lat_step * self.lat_index

    @property
    def lon(self):
        return self.matrix.lon_offset + self.matrix.lon_step * self.lon_index - (self.lat_index % 2) * (self.matrix.lon_step / 2)

    def __repr__(self):
        return f"Cell({self.lat_index}, {self.lon_index}): lat={self.lat:.4f}, lon={self.lon:.4f}"

    def __hash__(self):
        return hash((self.lat_index, self.lon_index, *self.matrix.shape))

    def __eq__(self, other):
        return (self.lat_index == other.lat_index
                and self.lon_index == other.lon_index
                and self.matrix.shape == other.matrix.shape)


class HexGrid(Grid):

    def __init__(self, num_lat_grid: int, num_lon_grid: int):
        self.shape = (num_lat_grid, num_lon_grid)
        self.lat_offset, self.lat_step = self._calculate_latitude_offset_and_step(num_lat_grid)
        self.lon_offset, self.lon_step = self._calculate_longitude_offset_and_step(num_lon_grid)

    def _calculate_latitude_offset_and_step(self, num_lat_grid):
        r = 180 / ((num_lat_grid - 1) * 3 / 2 + 2)
        return 90 - r, 3 / 2 * r

    def _calculate_longitude_offset_and_step(self, num_lon_grid):
        r = 180 / num_lon_grid
        return r - 180, 2 * r

    def get_lat_and_lon(self, lat_index: int, lon_index: int):
        """주어진 인덱스에 대한 Cell의 위경도 정보를 반환
        """
        lat = self.lat_offset - lat_index * self.lat_step
        lon = self.lon_offset + lon_index * self.lon_step
        if lat_index % 2:
            lon -= self.lon_step / 2
        return lat, lon

    def get_index(self, lat:float, lon:float):
        """주어진 위경도가 속하는 Cell의 index 반환
        """
        indices = self._get_candidate_indices(lat, lon)
        cells = [HexCell(i, j, self) for i, j in indices]
        target_index = self._get_target_index(lat, lon, cells)

        return indices[target_index]

    def get_cell(self, lat:float, lon:float) -> HexCell:
        """주어진 위경도가 속하는 HexCell 반환
        """
        indices = self._get_candidate_indices(lat, lon)
        cells = [HexCell(i, j, self) for i, j in indices]
        target_index = self._get_target_index(lat, lon, cells)

        return cells[target_index]

    def _get_candidate_indices(self, lat, lon):
        from numpy import floor, ceil

        rough_lat_index = (self.lat_offset - lat) / self.lat_step
        rough_lon_index = (lon - self.lon_offset + (floor(rough_lat_index) % 2) * self.lon_step / 2) / self.lon_step

        return [(int(f1(rough_lat_index) % self.shape[0]), int(f2(rough_lon_index) % self.shape[1]))
                for f1, f2 in [[floor, floor], [floor, ceil], [ceil, floor], [ceil, ceil]]]

    def _get_target_index(self, lat, lon, cells):
        distances = np.sqrt(
            np.square(np.array([cell.lat for cell in cells]) - lat) +
            np.square(np.array([cell.lon for cell in cells]) - lon)
        )
        return int(np.argmin(distances))