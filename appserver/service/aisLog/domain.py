from datetime import datetime

from pydantic import BaseModel, validator

from appserver.commons import RequestError


class AisLog(BaseModel):
    """ 현재 배의 로그 정보
    """
    imo: int

    lat: float
    lon: float
    heading: int
    reg_dt: datetime

    @validator("lat")
    def latitude_match(cls, v):
        if v < -90 or v > 90:
            raise RequestError("위도 범위는 -90~90도여야 합니다.")
        return v

    @validator("lon")
    def longitude_match(cls, v):
        if v < -180 or v > 180:
            raise RequestError("경도 범위는 -180~180도여야 합니다.")
        return v

    @validator("heading")
    def heading_match(cls, v):
        if v < 0 or v > 360:
            raise RequestError("각도 범위는 0~360도여야 합니다.")
        return v
