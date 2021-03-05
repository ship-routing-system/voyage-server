from ...grid import *
from scipy.sparse import csr_matrix
import pandas as pd


def generate_layer_by_counting(route_df:pd.DataFrame, grid:HexGrid):
    """
    항로 정보(route_df)을 grid에 맞게 재배치하여,cost_matrix을 생성하는 함수

    """
    lat_lon = route_df.groupby(['lat', 'lon']).size().reset_index(name='cnt')
    hex_locations = [grid.get_index(row.lat, row.lon) for idx, row in lat_lon.iterrows()]
    lat_lon = lat_lon.assign(hex_id=hex_locations)

    lat_lon_sum = lat_lon.groupby('hex_id').cnt.sum().reset_index(name='cnt')

    row = lat_lon_sum['hex_id'].map(lambda x: x[0]).values
    col = lat_lon_sum['hex_id'].map(lambda x: x[1]).values
    data = lat_lon_sum.cnt.values
    return csr_matrix((data, (row, col)), shape=grid.shape)