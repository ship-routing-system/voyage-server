import unittest
from datetime import datetime

from appserver.commons import RequestError
from appserver.service.aisLog import AisLog


class AisLogTestCase(unittest.TestCase):
    def test_validation_on_latitude(self):
        # -91도 (Request Error)
        self.assertRaises(RequestError, lambda: AisLog(imo=1, lat=-91, lon=1., heading=1, reg_dt=datetime.now()))
        # +91도 (Request Error)
        self.assertRaises(RequestError, lambda: AisLog(imo=1, lat=91, lon=1., heading=1, reg_dt=datetime.now()))
        # +30도 (정상)
        AisLog(imo=1, lat=30, lon=1., heading=1, reg_dt=datetime.now())

    def test_validation_on_longitude(self):
        # -181도 (Request Error)
        self.assertRaises(RequestError, lambda: AisLog(imo=1, lat=1, lon=-181., heading=1, reg_dt=datetime.now()))
        # +181도 (Request Error)
        self.assertRaises(RequestError, lambda: AisLog(imo=1, lat=1, lon=+181., heading=1, reg_dt=datetime.now()))
        # +30도 (정상)
        AisLog(imo=1, lat=1., lon=31., heading=1, reg_dt=datetime.now())

    def test_validation_on_heading(self):
        # -1도 (Request Error)
        self.assertRaises(RequestError, lambda: AisLog(imo=1, lat=1, lon=31., heading=-1, reg_dt=datetime.now()))
        # +361도 (Request Error)
        self.assertRaises(RequestError, lambda: AisLog(imo=1, lat=1, lon=31., heading=361, reg_dt=datetime.now()))
        # +10도 (정상)
        AisLog(imo=1, lat=1., lon=31., heading=1, reg_dt=datetime.now())


if __name__ == '__main__':
    unittest.main()
