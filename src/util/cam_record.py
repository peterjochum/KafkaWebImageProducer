import base64
import json
from dataclasses import dataclass


@dataclass
class CamRecord:
    cam_id: int
    desc: str
    image_data: bytes
    area: list

    def to_json(self):
        res = {}
        res["cam_id"] = self.cam_id
        res["desc"] = self.desc
        res["area"] = self.area
        res["image_data"] = base64.b64encode(self.image_data).decode('ascii')
        json_data = json.dumps(res)
        return json_data

    @staticmethod
    def from_json(data):
        dct = json.loads(data)
        cam_id = dct["cam_id"]
        desc = dct["desc"]
        area = dct["area"]
        image_data = base64.b64decode(dct["image_data"])
        return CamRecord(cam_id, desc, image_data, area)