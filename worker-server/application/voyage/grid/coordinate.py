from abc import ABC, abstractmethod
from typing import List, Tuple


class Cell(ABC):
    def __init__(self):
        self.lat_index = None
        self.lon_index = None

    @abstractmethod
    def neighbors(self) -> List: pass

    @property
    @abstractmethod
    def lat(self): pass

    @property
    @abstractmethod
    def lon(self): pass

    def __lt__(self, other):
        """ priorityQueue에서 HexCell간 비교를 위해 오버라이딩한 매직메서드
        """
        return True


class Grid(ABC):
    @abstractmethod
    def get_lat_and_lon(self, lat_index: int, lon_index: int) -> Tuple[int, int]: pass

    @abstractmethod
    def get_index(self, lat:float, lon:float) -> Tuple[int, int]: pass

    @abstractmethod
    def get_cell(self, lat:float, lon:float) -> Cell: pass