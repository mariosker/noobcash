from time import sleep, time

from config import config

import requests
from requests.adapters import HTTPAdapter, Retry


def poll_endpoint(url: str, request_type='post', data=None):
    """makes a request to an endpoint and waits for a response. In case of failure retries

    Args:
        url (str): the endpoint to hit
        request_type (str, optional): The type of the request. Supports post and get requests. Defaults to 'post'.
        data (_type_, optional): Data to attach to the request. Defaults to None.

    Returns:
        response: the response of the request
    """
    s = requests.Session()
    r = None
    retries = Retry(total=10,
                    backoff_factor=2,
                    status_forcelist=[429, 500, 502, 503, 504])
    s.mount('http://', HTTPAdapter(max_retries=retries))
    if request_type == 'post':
        r = s.post(url, data=data)
    else:
        r = s.get(url, data=data)
    return r
