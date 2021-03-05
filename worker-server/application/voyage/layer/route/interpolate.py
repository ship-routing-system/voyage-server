import pandas as pd
from scipy.interpolate import interp1d
import numpy as np


class Interpolator:
    """
    항해 경로에 대한 Interpolation을 수행하는 클래스

    """
    period = None
    kind = None
    NANO = 10 ** 9

    def __init__(self, period=3600, kind='linear'):
        """
        period : 보정할 시간간격(초 기준)
        kind : ('linear', 'nearest', 'zero', 'slinear', 'quadratic', 'cubic','previous', 'next'
        """
        self.period = period
        self.kind = kind

    def interpolate(self, route_df: pd.DataFrame):
        """
        route_df : 하나의 imo에 대한 항해 정보
        """
        seconds = route_df.reg_dt.astype(np.int) // self.NANO
        lats, lons = route_df.lat, route_df.lon

        imo_no = route_df.imo_no.values[0]
        i_secs = self._generate_interpolated_seconds(seconds)
        i_lats = interp1d(seconds, lats, self.kind)(i_secs)
        i_lons = interp1d(seconds, lons, self.kind)(i_secs)

        df = self._create_interpolated_df(imo_no, i_secs, i_lats, i_lons)

        df['reg_dt'] = pd.to_datetime(df['reg_dt'] * self.NANO)
        return df

    def _generate_interpolated_seconds(self, seconds):
        return np.arange(seconds.min(), seconds.max(), self.period)

    def _create_interpolated_df(self, imo_no, seconds, lat_positions, lon_positions):
        interpolated_df = pd.DataFrame({
            'reg_dt': seconds,
            'lat': lat_positions,
            'lon': lon_positions
        })
        interpolated_df['imo_no'] = imo_no
        return interpolated_df[['imo_no', 'lat', 'lon', 'reg_dt']]