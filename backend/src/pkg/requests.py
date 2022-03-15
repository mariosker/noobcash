from time import sleep, time

from config import config

import requests


def poll_endpoint(URL: str, obj=None, requests_function=requests.post, time_window=5, timeout=30):
    start = time()
    while True:
        if timeout > start:
            raise ValueError('timeout reached')
        try:
            resp = requests_function(URL, data=obj)
            return resp
        except Exception as err:
            config.logging.debug(err)
        sleep(time_window)
