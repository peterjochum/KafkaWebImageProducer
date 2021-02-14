from unittest import TestCase
from .cam_config import CamConfig


class CamConfigTestCase(TestCase):
    def test_init(self):
        c = CamConfig.from_file("../cam_config_example.json")
        self.assertEqual(c.cam_id, 2)
        self.assertEqual(c.desc, "test_description")
        self.assertEqual(c.url, "http://testurl.com")
