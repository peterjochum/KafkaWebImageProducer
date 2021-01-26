import time

from kafka import KafkaProducer
from os import environ
from urllib.request import urlretrieve
import logging

env_bootstrap_server = "BOOTSTRAP_SERVERS"
env_interval = "RETRIEVE_INTERVAL"
env_image_url = "IMAGE_URL"
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
    retrieve_interval = environ.get(env_interval)
    if not retrieve_interval:
        retrieve_interval = default_retrieve_interval
        logging.info(f"{env_interval} not set, using {default_retrieve_interval} seconds")
    else:
        logging.info(f"{env_interval} set, using {retrieve_interval} seconds")
    return retrieve_interval


if __name__ == '__main__':
    boostrap_server = environ.get(env_bootstrap_server)
    if not boostrap_server:
        raise EnvironmentError(f"Set {env_bootstrap_server} in environment")

    retrieve_interval = get_retrieve_interval()
    image_url = environ.get(env_image_url)
    producer = KafkaProducer(bootstrap_servers=boostrap_server)
    while True:
        img_data = get_image(image_url)
        r = producer.send('trafficcam', img_data)
        if r.succeeded():
            logging.info(f"Wrote image with timestamp {r}")
        time.sleep(retrieve_interval)
