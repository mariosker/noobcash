from time import sleep, time

from config import config

import requests


def poll_endpoint(URL: str, requests_function=requests.post, data=None, time_window=5, timeout=15):
    start = time()
    while True:
        curr_time = time()
        if curr_time > start + timeout:
            raise ValueError('timeout reached')
        try:
            resp = requests_function(URL, data=data)
            return resp
        except Exception as err:
            config.logging.debug(err)
        sleep(time_window)
