#!/usr/bin/env python3
import logging
from functools import wraps
from urllib.parse import urljoin
from .funcs import *


class attr:

    links = "//a[@href!='#'][@href!='javascript:;'][@href!='#']"
    green = "\033[0;32m%s\033[0m"
    red = "\033[0;31m%s\033[0m"
    yellow = "\033[0;33m%s\033[0m"
    checktor = {
        " and 1=1--- and 1=2": eq,
    }

def getHeaders(host, text=None, **kargs):
    headers_2 = { i.split(':')[0]: i.split(':')[1] for i in text.split("\n")}
    raw_headers  = {
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': host,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
    }
    for k in headers_2:
        raw_headers[k] = headers_2[k]
        
    for k in kargs:
        raw_headers[k] = kargs[k]
    return raw_headers

def check_url(url_head, url, ssl=False):
    http_head = "https://" if ssl else "http://"
    domain = url_head if url_head.startswith("http") else http_head + "www." + url_head + ".com"
    # check first arg
    arg = url
    if arg.startswith("http"):
        if arg.find(url_head) > -1:
            return arg
        logging.warn(attr.yellow % "This link [out]" + arg)
        return None
    if arg.startswith("/"):
        return urljoin(domain, arg)
    elif arg.startswith("www"):
        if arg.find(url_head) > -1:
            return http_head + arg
        logging.warn(attr.red % "This link invalid! [out]" + arg)
        return None
    else:
        arg = urljoin(domain, arg) 
        return arg


