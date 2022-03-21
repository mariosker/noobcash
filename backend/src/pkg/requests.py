from time import sleep, time

from config import config

import requests
from requests.adapters import HTTPAdapter, Retry


def poll_endpoint(url: str, request_type='post', data=None):

    s = requests.Session()
    r = None
    retries = Retry(total=5,
                    backoff_factor=2,
                    status_forcelist=[429, 500, 502, 503, 504])
    s.mount('http://', HTTPAdapter(max_retries=retries))
    if request_type == 'post':
        r = s.post(url, data=data)
    else:
        r = s.get(url, data=data)
    return r
