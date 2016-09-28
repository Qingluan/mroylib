#!/usr/bin/env python3
import requests
import logging
import time
from lxml import etree
from .config import attr
from .config import check_url


def setLogging(file_name=time.asctime().replace(" ","_") + ".log", level=logging.WARNING):
    logging.basicConfig(
        level=level,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%a,%d,%Y',
        filename=file_name,
        filemode='a')

class Links_stack:
    got = set()
    session = None
    headers = None
    init = 1

    @staticmethod
    def init_session(init_url, headers=None):
        s = requests.Session()
        s.get(init_url, headers=headers)
        Links_stack.session = s
        return Links_stack.session

    @staticmethod
    def set_headers(headers):
        Links_stack.headers = headers


def get_headers(host, text=None, **kargs):
    headers_2 = {}
    if text:
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


def get_links(url, verify=False, init_url=None):
    if url != None:
        etr = None
        try:
            s = None

            if not Links_stack.session:
                s = Links_stack.init_session(init_url) if init_url else requests.Session()
                Links_stack.session = s
            else:
                s = Links_stack.session
            if Links_stack.init == 1:
                raw_response = s.get(url, verify=verify, headers=Links_stack.headers)
                print(Links_stack.headers)
                Links_stack.init = -1
            else:
                raw_response = s.get(url, verify=verify)
            print(attr.yellow %  '[%d]' % raw_response.status_code + attr.green % url)
            etr = etree.HTML(raw_response.content.decode(raw_response.encoding))
        except Exception as e:
            logging.fatal(attr.red % url)
            print(e)
            yield None

        if etr != None:
            logging.warn(attr.green % "load page:[got]" + url)
            for link in etr.xpath(attr.links):
                yield link.attrib['href']
        else:
            yield None
    else:
        yield None
    
def gen_points(head, url, ssl=False, exe=None):
    if url == None:
        yield None
    else:
        if not exe:
            for link in get_links(url, ssl):
                if link == None:
                    continue
                if link in Links_stack.got:
                    continue
                Links_stack.got.add(link)
                yield from gen_points(head, check_url(head, link, ssl), ssl=ssl, exe=exe)
        else:
            for link in exe.submit(get_links, url, ssl):
                if link == None:
                    continue
                if link in Links_stack.got:
                    continue
                Links_stack.got.add(link)
                yield from gen_points(head, check_url(head, link, ssl), ssl=ssl, exe=exe) 