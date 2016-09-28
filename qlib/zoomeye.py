import requests as R
import urllib
import sys
import json
import logging

try:
    from qmongohelper import Mongo
except Exception as  e:
    logging.warn("you should install 'qmongo_heler', this  you can found in github")
else:
    pass
finally:
    pass
class Base:
    main_url = 'https://api.zoomeye.org'
    urls = {
        'login': '/user/login',
        'host': 'GET /host/search',
    }


class Zoomeye(Base):

    def __init__(self, u, p):
        self.u = u
        self.p = p
        self.session = R.Session()
        self.token = json.loads(self.session.post(Base.main_url+Base.urls['login'],
                                        data=json.dumps({
                                            'username':u,
                                            'password':p})).content.decode("utf8"))['access_token']
        self.session.headers['Authorization'] = 'JWT ' + self.token
        self.headers = self.session.headers
    
    def _u(self, url):
        return urllib.parse.urljoin(Base.main_url, url) 

    def _read_config(self, label):
        method_type, url = Base.urls[label].split()
        return getattr(self.session, method_type.lower()), self._u(url)

    def _tr(self, dic):
        return '&'.join([ '='.join([pair[0], str(pair[1])])  for pair in  dic.items() ])

    def scan(self, typ, **kargs):
        func, url = self._read_config(typ)
        args = self._tr(kargs)
        logging.info(args)
        # print(url,args)
        url = url + '' if args.endswith('&') else url + '?' #, headers=self.headers)
        logging.debug(url  + args)
        return func(url + args).json()

class Scanner(Zoomeye):

    def __init__(self, *args, db=None, **kargs):
        super(Zoomeye,self).__init__(*args, **kargs)
        if db:
            self.db = dbheler(db)

    def hosts(self, **kargs):
        res_json = super(Scaner, self).scan("host", **kargs)
        self.db.insert("hosts", **res_json)


def main():
    pass
if __name__ == '__main__':
    main()
