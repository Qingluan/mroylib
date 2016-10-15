# -*- coding: utf8 -*- 
from qlib.net import to, parameters
from qlib.net.agents import AGS
from qlib.graphy import random_choice
from qlib.asyn import Exe
from qlib.log import LogControl

from lxml.etree import HTML
from urllib.parse import quote

LogControl.LOG_LEVEL = LogControl.OK
LogControl.LOG_LEVEL |= LogControl.FAIL
LogControl.LOG_LEVEL |= LogControl.INFO

class Searcher:
    config = {
        'search_url': '',
        'search_args': {},
    }

    def __init__(self, ssl=True, asyn=False, debug=False):
        self.url_pre = 'https://www.' if ssl else  'https//www.'
        self.host = self.url_pre + self.__class__.__name__.lower() + '.com'
        self.agent = random_choice(AGS)
        self.asyn = None
        self.debug =debug
        if asyn:
            self.asyn = Exe(10)

    def xpath(self, html, *tags,exclude=None):
        xhtml = HTML(html)
        exclude = '[not(name()={})]'.format(exclude) if exclude else ''
        LogControl.info("//" + "//".join(tags) + exclude) if self.debug else ''
        for item in xhtml.xpath("//" + "//".join(tags) + exclude):
            yield item

    def ready(self, pre_url, *args, **options):
        pass

    def set_args(self, **kargs):
        return parameters(**kargs)

class Google(Searcher):
    pass


class Baidu(Searcher):
    
    config = {
        'translate_tag': "@class='op_dict_content'",
        'translate_url': "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd={query}\
                            &rsv_pq=be1d9cdc00001f3a&rsv_t=e851oZevI5oKNV9F6W9CwY5wqlPyiK9Pqz0RLr7vdyawQru3NgKGrAcsizA\
                            &rqlang=cn&rsv_enter=1&rsv_sug3=20&rsv_sug2=0&inputT=2703&rsv_sug4=6023"
    }
    

    def translate(self, raw, to_lang='英文'):
        if not self.asyn:
            self.asyn = Exe(10)

        def query(url):
            res = to(url)
            en = res.encoding
            return res.status_code, res.content.decode(en) 

        def display(code, content):
            '''
            display content
            '''
            if int(code / 200) == 1:
                res = '\n'.join([ i.text for i in self.xpath(content, "div[%s]" % Baidu.config['translate_tag'], 'td', '*')])
                LogControl.ok(res)
            else:
                LogControl.fail("not found this")

        data = Baidu.config['translate_url'].format(query=quote(raw + ' ' + to_lang))
        self.asyn.done(query, display, data)



class BaiduTranslate(Searcher):

    def translate(self, raw, from_lan='en', to_lan='zh', detail=False, example=False):
        """
        
        detail : if detail == true will get more information.
        example : if example == true will get some sample.

        """
        self.host = 'fanyi.baidu.com/v2transapi'
        if not self.asyn:
            self.asyn = Exe(10)

        def query(data):
            res = to(self.host, method='post', data=data)
            return res.status_code, res.json()

        def tree_dict(d, func, key=None, lfunc=None):
            if isinstance(d, dict):
                for item in d:
                    tree_dict(d[item], func, key=item)
            elif isinstance(d, list):
                for item in d:
                    if lfunc:
                        tree_dict(item, lfunc)
                    else:
                        tree_dict(item, func)
            else:
                if key:
                    if key == 'dst':
                        LogControl.ok(d, txt_color='green', txt_attr=['underline','bold'])
                    else:
                        func(d, key)
                else:
                    func(d)

        def single_display(val, key=None, level=1):
            if key:
                LogControl.ok('[' + key + ']', '\t', val)
            else:
                LogControl.info('\t\t' + '   ' * level, val)

        def display(code, content):
            '''
            display content
            '''
            if int(code / 200) == 1:
                try:
                    tree_dict(content['trans_result'], single_display, 'base')
                    if detail:
                        tree_dict(content['dict_result'], single_display, 'dict')
                    if example:
                        tree_dict(content['liju_result'], single_display, 'sample')
                except KeyError:
                    LogControl.fail("Only: ", *content.keys())
                    for k in content:
                        LogControl.err(k, content[k])

            else:
                LogControl.fail("not found this")

        data = {
            'from': from_lan,
            'to': to_lan,
            'query': raw,
            'transtype':'translang', 
            'simple_means_flag':'3',
        }
        self.asyn.done(query, display, data)


class DuckDuckGo(Searcher):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.search_url = 'https://duckduckgo.com/d.js?q={query}&{options}&vqd={vqd}'
        self.search_args = 'l=wt-wt&p=1&s=0&a=h_&ct=US&ss_mkt=us'



    def search(self, query):
        url_query = quote('+'.join(query.split()))

        def get_vqd(query):
            sss = to('http://duckduckgo.com/?q={query}&t=h_&ia=web'.format(query=query)).content.decode('utf8')
            return sss[sss.rfind("vqd"):].split("&").pop(0).split("=").pop()

        args = self.search_args
        vqd = get_vqd(url_query)
        url = self.search_url.format(query=url_query, options=self.search_args, vqd=vqd) + '&sp=1&yhs=1'
        LogControl.info(url) if self.debug  else ''
        return to(url, headers={'cookie':'ak=-1'})


