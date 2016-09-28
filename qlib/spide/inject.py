#!/usr/bin/env python3
import requests
import logging
import time
from hashlib import md5
from urllib.parse import quote

logging.level = 1

def check_time(func):
    sta = time.time()
    def _ch(*args, **kargs):
        res = func(*args, **kargs)
        logging.info(time.time() - sta)
        return res
    return _ch

@check_time
def _hash_point(url, additional):
    url = url + quote(additional)
    return md5(requests.get(url).content).hexdigest()



def check_injecable(url, checktor):
    for method in checktor:
        logging.warn("check:" + method)
        judge = checktor[method]
        args  = [_hash_point(url, sql) for sql in method.split("---")]
        logging.warn("hash ok : " + url)
        if judge(*args):
            return True
    return False


