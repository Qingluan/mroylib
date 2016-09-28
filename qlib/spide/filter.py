#!/usr/bin/env python3
import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor


def got(url):
    file_url = url.replace("/", "_")
    with open(file_url, "wb") as tar: 
        tar.write(requests.get(url, verify=False).content)


def read_list(f):
    with open(f) as fp:
        for line in fp:
            yield line


def download(lst):
    with ThreadPoolExecutor(10) as exe:
        wc = 0
        for link in lst:
            print("sub : %s %d" % (link, wc),end="\r")
            exe.submit(got, link)
            wc += 1
        exe.shutdown()
