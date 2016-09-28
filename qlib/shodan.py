import requests as R
import urllib
from zoomeye import Zoomeye, Base

class Shodan(Zoomeye):
    
    def __init__(self):
        Base.main_url = "https://api.shodan.io"
        Base.urls = {
            "host":"GET /shodan/host/search",
        }
        Base.token =  "XHSWncMjN6MEyekECTMcOeoEocl6VO2q"
    
        self.session = R.Session()
        self.headers = self.session.headers

    def _u(self, url):
        url = super(Shodan, self)._u(url)
        token_url = urllib.parse.urljoin(url, "?key=%s&" % Shodan.token)
        return token_url