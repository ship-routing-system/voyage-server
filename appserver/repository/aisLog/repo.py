from typing import List, Optional

from sqlalchemy import Column, Integer, Float, DateTime, desc
from sqlalchemy.orm import sessionmaker

from appserver.repository import Base
from appserver.service.aisLog import AisLog


class AisLogEntity(Base):
    """ AIS Log에 관련된 entity
    ````sql
        CREATE TABLE `ais_log` (
            `no` INT(64) UNSIGNED NOT NULL AUTO_INCREMENT,

            `imo` INT(32) UNSIGNED NOT NULL,

            `lat` DOUBLE DEFAULT NULL,
            `lon` DOUBLE DEFAULT NULL,
            `heading` INT DEFAULT NULL,
            `reg_dt` TIMESTAMP DEFAULT NULL,

            PRIMARY KEY (`no`),
            KEY `IDX_AIS_LOG` (`reg_dt`)
        );
    ````
    """
    __tablename__ = "ais_log"

    no = Column(Integer, primary_key=True, autoincrement=True)

    imo = Column(Integer)

    lat = Column("lat", Float)
    lon = Column("lon", Float)
    heading = Column("heading", Integer)
    reg_dt = Column("reg_dt", DateTime)

    def __repr__(self):
        fields = vars(self)
        fields.pop('_sa_instance_state', None)
        return f'''<AisLogEntity({fields})>'''


class AisLogRepository:
    """ AIS Log에 ROW을 읽거나, 저장하는 역할
    """
    TABLE = AisLogEntity

    def __init__(self, engine):
        self.engine = engine

    def read_recent(self, imo) -> Optional[AisLog]:
        """ 해당 배에 대한 최근 AISLOG을 가져오기
        Args:
            imo: 타겟 배의 imo_no
        Returns:
            AisLog
        """
        with sessionmaker(self.engine).begin() as sess:
            row = sess.query(self.TABLE).filter(self.TABLE.imo == imo).order_by(desc(self.TABLE.reg_dt)).first()
            if row:
                return AisLog(imo=row.imo, lat=row.lat, lon=row.lon, heading=row.heading, reg_dt=row.reg_dt)
            else:
                return None

    def read(self, imo) -> List[AisLog]:
        """ 해당 배에 대한 모든 AisLog 가져오기
        Args:
            imo:
        Returns:
            List[AisLog]
        """
        res = []
        with sessionmaker(self.engine).begin() as sess:
            for row in sess.query(self.TABLE).filter(self.TABLE.imo == imo).all():
                log = AisLog(imo=row.imo, lat=row.lat, lon=row.lon, heading=row.heading, reg_dt=row.reg_dt)
                res.append(log)
        return res

    def save(self, ais_log: AisLog):
        """ ais_log를 Database에 저장
        Args:
            ais_log:

        Returns:
            None
        """
        with sessionmaker(self.engine).begin() as sess:
            entity = AisLogEntity(imo=ais_log.imo,
                                  lat=ais_log.lat,
                                  lon=ais_log.lon,
                                  heading=ais_log.heading,
                                  reg_dt=ais_log.reg_dt)
            sess.merge(entity)
