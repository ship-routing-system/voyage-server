import unittest
from datetime import datetime

from sqlalchemy import create_engine

from appserver.repository import Base
from appserver.repository.aisLog import AisLogRepository
from appserver.service.aisLog import AisLog


class AisLogRepositoryTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:", echo=True)
        self.repository = AisLogRepository(self.engine)
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_저장이_올바르게_수행되는지를_확인해보자(self):
        given = AisLog(imo=1, lat=1, lon=1, heading=1, reg_dt=datetime.now())
        self.repository.save(given)

        result = self.repository.read(1)[0]

        self.assertEqual(given, result)

    def test_최근_것을_가져오는지를_확인해보자(self):
        given1 = AisLog(imo=1, lat=1, lon=1, heading=1, reg_dt=datetime(2021, 1, 5))
        given2 = AisLog(imo=1, lat=1, lon=1, heading=1, reg_dt=datetime(2021, 1, 6))
        given3 = AisLog(imo=1, lat=1, lon=1, heading=1, reg_dt=datetime(2021, 1, 2))
        self.repository.save(given1)
        self.repository.save(given2)
        self.repository.save(given3)

        result = self.repository.read_recent(1)

        self.assertEqual(given2, result)

    def test_없는_것을_조회하였을_때에는_빈_리스트를_반환한(self):
        result = self.repository.read(2)

        self.assertEqual(len(result), 0)

    def test_없는_것을_조회하였을_때_최근_값을_조회하면_None을_반환한다(self):
        result = self.repository.read_recent(2)

        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
