import logging
import os
import time
from datetime import datetime
from os import environ
from urllib.error import URLError
from urllib.request import urlretrieve

from kafka import KafkaProducer

from util.cam_config import CamConfig
from util.cam_record import CamRecord

env_name_bootstrap_server = "BOOTSTRAP_SERVERS"
env_name_interval = "RETRIEVE_INTERVAL"
env_name_config_file = "CAM_CONFIG_FILE"
env_name_target_topic = "CAM_TOPIC"

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

    cam_config_file = environ.get(env_name_config_file)
    if not cam_config_file:
        raise EnvironmentError(f"Set {env_name_config_file} in environment")

    if not os.path.exists(cam_config_file):
        raise EnvironmentError(f"File {cam_config_file} was not found")

    topic = environ.get(env_name_target_topic)
    if not topic:
        raise EnvironmentError(f"Set a topic with {env_name_target_topic} variable")

    retrieve_interval = get_retrieve_interval()
    c = CamConfig.from_file(cam_config_file)
    logging.info(f"Getting images from {c.url} ...")
    producer = KafkaProducer(bootstrap_servers=boostrap_server)
    # value_serializer=lambda rec: dumps(rec.to_json()).encode('utf-8')
    while True:
        try:
            img_data = get_image(c.url)
            new_record = CamRecord(c.cam_id, c.desc, img_data, c.area)
            r = producer.send(topic, new_record.to_json().encode("utf-8"), partition=c.cam_id % 10)
            with open(f"images/{datetime.now().timestamp()}_{c.cam_id}.jpg", 'wb') as f:
                f.write(img_data)
            while not r.is_done:
                time.sleep(0.1)
            logging.info(f"Wrote image with offset {r.value.offset} and timestamp {r.value.timestamp}")
        except URLError:
            logging.warning(f"Could not fetch image from URL {c.url} .. retrying in {retrieve_interval} seconds")
        time.sleep(retrieve_interval)
