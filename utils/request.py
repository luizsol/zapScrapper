import requests
import json
import time

GET = 'GET'
OPTIONS = 'OPTIONS'
POST = 'POST'
PUT = 'PUT'
PATCH = 'PATCH'
DELETE = 'DELETE'
HEAD = 'HEAD'


def fetch(url, method=GET, data=None, headers=None, verify=None, timeout=5.0):
    """Retrieves data from a web service.

    Args:
        url: str

    Kwargs:
        method: 'GET' | 'OPTIONS' | 'POST' | 'PUT' | 'PATCH' | 'DELETE' |
            'HEAD', default to 'GET'
        data: str | dict | None, default to None
        headers: str | None, default to None
        verify: bool | None, default to None
        timeout: float | int, default to 5.0

    Returns:
        if the status code of the request is 200:
            requests object
        else:
            raises a RuntimeError
    """
    if type(data) is dict:
        data = json.dumps(data)

    request = requests.request(method, url, timeout=5.0, data=data,
                               headers=headers, verify=verify)

    if request.status_code == requests.codes.ok:
        return request
    else:
        raise RuntimeError(f'Request status not ok ({request.status_code}).')


def fetch_json(url, method=GET, data=None, headers=None, verify=None,
               timeout=5.0):
    """Retrieves json data from a web service.

    Args:
        url: str

    Kwargs:
        method: 'GET' | 'OPTIONS' | 'POST' | 'PUT' | 'PATCH' | 'DELETE' |
            'HEAD', default to 'GET'
        data: str | dict | None, default to None
        headers: str | None, default to None
        verify: bool | None, default to None
        timeout: float | int, default to 5.0

    Returns:
        if the status code of the request is 200:
            a dict representing the parsed data
        else:
            raises a RuntimeError
    """
    request = fetch(**locals())

    return json.loads(request.text)


