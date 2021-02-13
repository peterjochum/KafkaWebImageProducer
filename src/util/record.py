import base64
import json
from dataclasses import dataclass


@dataclass
class Record:
    cam_id: int
    image_data: bytes

    def to_json(self):
        res = {}
        res["cam_id"] = self.cam_id
        res["image_data"] = base64.b64encode(self.image_data).decode('ascii')
        json_data = json.dumps(res)
        return json_data

    @staticmethod
    def from_json(data):
        dct = json.loads(data)
        cam_id = dct["cam_id"]
        image_data = base64.b64decode(dct["image_data"])
        return Record(cam_id, image_data)