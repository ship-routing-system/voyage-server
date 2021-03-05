from google.cloud import bigquery
import pandas as pd
from .environment import region, table_name, dataset_name


def read_ship_voyage_data(imo_no:int) -> pd.DataFrame:
    """
    특정 배에 대한 항해 기록을 빅쿼리로부터 읽어오는 함수

    Args:
        imo_no: 가져오고자 하는 선박의 imo_no

    Returns:
        해당 선박에 대한 DataFrame
    """
    client = bigquery.Client(location=region())
    return client.query(f'''
        SELECT imo_no, lat, lon, reg_dt
        FROM `{dataset_name()}.{table_name()}`
        WHERE
            imo_no = {imo_no} AND 
            imo_partition_id = {imo_no % 10000};
    ''').to_dataframe()
