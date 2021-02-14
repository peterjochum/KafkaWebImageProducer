from datetime import datetime
import time
from json import dumps
from urllib.error import URLError


from kafka import KafkaProducer
from os import environ
from urllib.request import urlretrieve
import logging

from src.util.cam_record import CamRecord
from util.cam_config import CamConfig

env_name_bootstrap_server = "BOOTSTRAP_SERVERS"
env_name_interval = "RETRIEVE_INTERVAL"

default_retrieve_interval = 60

def get_image(url):
    """
    Retrieve an image from a URL and return its contents
    :param url: Image URL
    :return:
    """
    img = urlretrieve(url)
    with open(img[0], "rb") as f:
        return f.read()


def get_retrieve_interval() -> int:
    interval = environ.get(env_name_interval)
    retrieve_interval = default_retrieve_interval
    if not interval:
        logging.info(f"{env_name_interval} not set, using {default_retrieve_interval} seconds")
    else:
        retrieve_interval = int(interval)
        logging.info(f"{env_name_interval} set, using {retrieve_interval} seconds")
    return retrieve_interval


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    boostrap_server = environ.get(env_name_bootstrap_server)
    if not boostrap_server:
        raise EnvironmentError(f"Set {env_name_bootstrap_server} in environment")

    retrieve_interval = get_retrieve_interval()
    c = CamConfig.from_file("cam_config.json")
    logging.info(f"Getting images from {c.url} ...")
    producer = KafkaProducer(bootstrap_servers=boostrap_server)
    # value_serializer=lambda rec: dumps(rec.to_json()).encode('utf-8')
    while True:
        try:
            img_data = get_image(c.url)
            new_record = CamRecord(c.cam_id, c.desc, img_data, c.area)
            r = producer.send('trafficcam', new_record.to_json().encode("utf-8"), partition=c.cam_id)
            with open(f"images/{datetime.now().timestamp()}_{c.cam_id}.jpg", 'wb') as f:
                f.write(img_data)
            while not r.is_done:
                time.sleep(0.1)
            logging.info(f"Wrote image with offset {r.value.offset} and timestamp {r.value.timestamp}")
        except URLError:
            logging.warning(f"Could not fetch image from URL {c.url} .. retrying in {retrieve_interval} seconds")
        time.sleep(retrieve_interval)
