import os, sys, time
import json, re
from queue import Queue, Empty
from termcolor import cprint
from urllib.parse import urljoin
from functools import wraps

sys.path.append(os.getenv("Q_PATH"))
from qlib.asyn import Exe, futures
from qlib.net import to
from qlib.graphy import random_choice
from qlib.spide.agents import AGS
from qlib.log import LogControl

LogControl.LOG_LEVEL = LogControl.OK
LogControl.LOG_LEVEL |= LogControl.WRN
LogControl.LOG_LEVEL |= LogControl.INFO
LogControl.LOG_LEVEL |= LogControl.FAIL

info = LogControl.info
err = LogControl.err
fail = LogControl.fail
ok = LogControl.ok
wrn = LogControl.wrn

try:
    from lxml.etree import HTML as _Parser
except ImportError :
    cprint("no lxml", "yellow")
    try:
        from bs4 import BeautifulSoup as _Parser
    except ImportError:
        cprint("no beautifulSoup", "red")
        sys.exit(0)


class HTTPError(Exception):
    """
    a base class for HTTP error
    """
    def __init__(self, msg, code):
        super().__init__(msg, code)
        self.code = code
        self.msg = msg

    def __str__(self):
        return "HTTP Error(%d): %s " % (self.code, self.msg)

class Error404(HTTPError):
    pass

class UrlValid(HTTPError):
    pass


def after(func):
    @wraps(func)
    def _after(futures):
        return func(futures.result())




class Handler:
    
    back_executor = None
    
    def __init__(self, thread_num=12, **kargs):
        self.host = None
        self.start_url = None
        self.domain = None

        self.unreadch_url = Queue()
        self.try_times = 10
        self.reach_url = set()
        self.stop = False
        self.outer_url = set()
        self.mail_url = set()
        self.js_url = set()
        self.all_links = set()

        self.charset = None
        
        self.db = None
        self.stop_count = 0
        self.parser = _Parser
        self.grep = None
        if not self.back_executor:
            Handler.back_executor = Exe(thread_num)

        # init args
        for k in kargs:
            if hasattr(self, k):
                setattr(self, k, kargs[k])

        if not self.start_url:
            raise UrlValid("not set start url", 0)
            sys.exit(0)

        if not self.domain:

            self.domain = self.start_url.split("/")[2]
            info("init domain :", self.domain)

        if not self.host:
            self.host = '/'.join(self.start_url.split("/")[:3])
            info("init host :", self.host)

        self._index(self.on_start)

    
    def _index(self, call):
        self.Got(self.start_url, call)
        

    def _after_deal(self, url):
        if not url:
            return
        if self.domain in url:
            self.reach_url.add(url)
        else:    
            self.outer_url.add(url)
        

    def ready_link(self, url):
        if url is None:
            return
        # info(url, len(url))
        url = url.strip()
        if url.startswith("None"):
            return
        if url.startswith("javascript"):
            self.js_url.add(url)
            return

        if url.startswith("#"):
            return

        if url.startswith("mailto:"):
            self.mail_url.add(url)
            return


        if url.startswith("http"):
            if self.domain in url.split("/")[2]:
                self.unreadch_url.put(url)
                self.all_links.add(url)
        elif url.startswith("/"):
            self.unreadch_url.put(urljoin(self.host, url))
            self.all_links.add(urljoin(self.host, url))
        elif url.startswith("www"):
            u = 'http://' + url
            if self.domain in  url.split("/")[0]:
                self.unreadch_url.put(u)
                self.all_links.add(u)
        else:
            pass
            # LogControl.err('ord :', url)

    def filter(self, url):
        return re.search(self.grep, url)

    def get_link(self):
        try:
            u = self.unreadch_url.get(timeout=120)
            if not u in self.reach_url:
                return u
        except Empty:
            cprint("long time no link , auto exited !", "green")
            sys.exit(0)

    def Got(self,real_url, after_done):
        """
        do a request from real_url, deal response in after_done asynchronously
        """
        Handler.back_executor.done(self._link, after_done, real_url)
        self._after_deal(real_url)

    def _link(self, url, encoding='utf8'):
        try:
            agent = random_choice(AGS)
            res = to(url, headers={'user-agent':agent})
            if res.status_code != 200:
                raise Error404("not reachable", res.status_code)
            if self.charset:
                return url, self.parser(res.content.decode(self.charset, 'ignore'))
            return url, self.parser(res.content.decode(encoding, 'ignore'))
        except HTTPError as e:
            LogControl.fail(url, e.code)
            return url, None
        except Exception as e:
            LogControl.wrn(url)
            LogControl.err(url, e, txt_color='yellow')
            return url, None
        else:
            LogControl.ok(url)

    def pause(self):
        self.stop = True

    def dead(self):
        self.stop = True
        self.unreadch_url = Queue()

    def run(self, callback, limit_wait=10):
        try:
            self.stop = False
            while not self.stop:
                if self.unreadch_url.empty():
                    info("\t\twait target pull", self.stop_count, end='\r')
                    time.sleep(1)
                    self.stop_count += 1
                    if self.stop_count > limit_wait:
                        self.stop = True
                    continue

                link = self.get_link()
                if not link:
                    continue
                self.Got(link, callback)

                if self.stop_count > limit_wait:
                    self.stop = True
            print()
        finally:
            self.stop = True
            self.stop_count = 0

    def to_db(self, k, v):
        self.db.set(k, v)

    def on_start(self, futures):
        raise NotImplementedError()

    def on_detail(self, futures):
        raise NotImplementedError()
