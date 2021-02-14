from unittest import TestCase

from .cam_record import CamRecord


class RecordTest(TestCase):
    def setUp(self) -> None:
        self.r = CamRecord(1, "test_desc", b"foo", [[1, 2], [3, 4]])
        self.r_json = '{"cam_id": 1, "desc": "test_desc", "area": [[1, 2], [3, 4]], "image_data": "Zm9v"}'

    def test_to_json(self):
        self.assertEqual(self.r_json, self.r.to_json())

    def test_from_json(self):
        r_from_json: CamRecord = CamRecord.from_json(self.r_json)
        self.assertEqual(1, r_from_json.cam_id)
        self.assertEqual("test_desc", r_from_json.desc)
        self.assertEqual(len(r_from_json.area), 2)
        self.assertEqual(b"foo", r_from_json.image_data)
