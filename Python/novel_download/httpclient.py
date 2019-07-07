# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 23:12:11 2019
    待办：
        获取网页不稳定
        添加伪装
        ip代理池
@author: 10127
"""
import time
import random
import requests as rq


default_header = {
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}

default_cookies = {'autologin':'1579236%3C%3E5936a323674e1233d68697a4ad7952730020cf24ced5813ada0da04873e8c2e8',
           'ks2':'zvah14bzm26h',
           'nlist1':'7pth.1',
           'sasieno':'0',
           }



class HttpClient():
    """ 网页获取类 """
    
    def __init__(self, urls, header=None):
        """ 初始化 """
        self._p = 0
        self._flag = 0
        self.urls = self._checkUrl(urls)
        self.header = self._checkheader(header)
#        self.pages = self.get()
        
    def _checkUrl(self, urls):
        """ 检查url的格式"""
        if type(urls) == str:
            return [urls]
        
        elif type(urls) == list or type(urls) == tuple:
            return urls
        else:
            raise TypeError
    
    def _checkheader(self, header):
        """ 检查header """
        if header == None:
            return default_header
        else:
            return header
    def _getpage_get(self, url):
        """ 获取网页，Get """
        i = 0
        while True:
            try:
                page = rq.get(url, header=self.header, timeout = (10,20))
            except rq.exceptions.ReadTimeout as e:
                i = i + 1
                if i > 10:
                    raise e
                
        #检查返回码
        if not page.ok:
            print('\tget page fail:', url)
#            page.raise_for_status()
            return None
        #转码
        print('\tget page:', url)
        page.encoding = "utf-8"
        return page.text                
    
    def _getpage_session(self, url, sesser):
        """ 获取网页，会话 """
        i = 0
        self._p += 1
        while True:
            try:
                page = sesser.get(url, timeout = (10,20))
                break
            except rq.exceptions.ReadTimeout as e:
#                time.sleep(6*60)
                i = i + 1
                if i > 10:
                    raise e
                
#        print(page.headers)
#        print(page.cookies.get_dict())
        #检查返回码
        if not page.ok:
            print('\tget page fail:', self._p)
            print('\t\tpage status code:' + str(page.status_code))
#            page.raise_for_status()
            return None
        #转码
        print('\tget page:', self._p)
        page.encoding = "utf-8"
        return page.text
    
    def page_generater(self):
        """ 获取网页（生成器） """
        with rq.Session() as s:
            s.headers.update(default_header)
            s.cookies.update(default_cookies)
            for url in self.urls:
                page = self._getpage_session(url, s)
                t = time.process_time()
                yield page
                if (time.process_time() - t) < 6:
                    time.sleep(4*random.randrange(3,5))
        return 0
        
    @property
    def pages(self):
        """ 通用网页获取函数"""
        pages = []
        with rq.Session() as s:
            s.headers.update(default_header)
            s.cookies.update(default_cookies)
            for url in self.urls:
                page = self._getpage_session(url, s)
                pages.append(page)
                time.sleep(3*random.randrange(3,5))
        return pages



if __name__ == '__main__':
    import json

    header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
             "Cookie": "autologin=1579236%3C%3E5936a323674e1233d68697a4ad7952730020cf24ced5813ada0da04873e8c2e8; ks2=zvah14bzm26h; sasieno=0; nlist1=7pth.1; ses=p8rhL0gUDeWZD41%2ClEeEH3"
            }
    with open(r"G:\Program\Git\my git\Web_page\JS\pageList.json") as f:
        pagelist = json.load(f)
    urls1 = []
    for i,v in pagelist.items():
        if i.find('.htm') > (len(i)-6):
            urls1.append('http://localhost:8842' + v.replace('\\', '/')[30:])
    temp1 = HttpClient(urls1,
                       header)
    ps = temp1.pages
    del header,i,v,urls1,pagelist
#    ,'https://ncode.syosetu.com/n1576cu/6/'
#    urls2 = ("https://ncode.syosetu.com/n0089bk/")
#    temp2 = HttpClient(urls2,header)
#
#    url_test1 = "https://ncode.syosetu.com/n0089bk/"
#    for i in range(100):
#        try:
#            temp = HttpClient(url_test1+str(i)+'/', header1)
#        except:
#            print("Ending：",i)
#            raise
#        print(time.strftime("%a, %d %b %Y %H:%M:%S"))
#        time.sleep(random.randrange(3,10))
        