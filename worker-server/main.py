from flask import Request
from application.data import read_ship_voyage_data
from application.voyage import HexGrid
from application.voyage import generate_layer_by_counting
from application.voyage import sparse2dict


def get_data(request: Request):
    param = request.get_json()
    imo_no = param['imo_no']
    df = read_ship_voyage_data(imo_no)
    return df.iloc[0].to_json(), 200


def calculate_cost(request: Request):
    param = request.get_json()
    imo_no = param['imo_no']
    map_size = param.get("map_size", (1000, 2000))

    route_df = read_ship_voyage_data(imo_no)
    grid = HexGrid(*map_size)

    sparse_matrix = generate_layer_by_counting(route_df, grid)
    return sparse2dict(sparse_matrix), 200
