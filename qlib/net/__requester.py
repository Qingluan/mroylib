import requests
from functools import wraps
from .config import RAW_HEADERS
from urllib.parse import urlencode
# _methods = {}


def parameters(**pars):
    return urlencode(pars)


def set_setssion():
    return requests.session()


def session(url):

    def _wrap(func):
        session = requests.Session()

        @wraps(func)
        def run(*args, **kargs):
            session.get(url)
            kargs['session'] = session
            return func(*args, **kargs)
        return run
    return _wrap


def to(url, data=None, ssl=False, method='get', **option):
    if not url.startswith("http"):
        if ssl:
            url = 'https://' + url
        else:
            url = 'http://' + url

    headers = RAW_HEADERS
    if 'headers' in option:
        for k in option['headers']:
            headers[k] = option['headers'][k]

    if "seesion" in option:
        m = option['session']
    else:
        m = getattr(requests, method)
        return m(url, data=data, headers=headers)


def network(url, data=None, method="get", **options):
    if "session" in options:
        m = getattr(options['session'], method)
    else:
        m = getattr(requests, method)

    if not data:
        req = m(url, headers=RAW_HEADERS)
    req = m(url, data=data, headers=RAW_HEADERS)

    def _wrap(func):
        func.res = req

        @wraps(func)
        def __call_back(*args, **kargs):
            return func(*args, **kargs)
        return __call_back
    return _wrap
