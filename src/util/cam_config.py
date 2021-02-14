from dataclasses import dataclass
from json import loads


@dataclass
class CamConfig:
    cam_id: int
    desc: str
    url: str
    area: list

    @staticmethod
    def from_file(file):
        with open(file) as f:
            dct = loads(f.read())
            return CamConfig(int(dct["camID"]), dct["desc"], dct["url"], dct["area"])
