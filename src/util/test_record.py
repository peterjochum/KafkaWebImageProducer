from unittest import TestCase

from .record import Record


class RecordTest(TestCase):

    def setUp(self) -> None:
        self.r = Record(1, b'foo')
        self.r_json = '{"cam_id": 1, "image_data": "Zm9v"}'

    def test_to_json(self):
        self.assertEqual(self.r_json, self.r.to_json())
        self.assertIsInstance(type(self.r.to_json()), bytes)

    def test_from_json(self):
        r_from_json: Record = Record.from_json(self.r_json)
        self.assertEqual(r_from_json.cam_id, 1)
        self.assertEqual(r_from_json.image_data, b'foo')