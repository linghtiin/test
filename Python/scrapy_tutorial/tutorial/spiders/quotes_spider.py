"""
    测试案例爬虫
    TODO:

"""

import scrapy
import re
from tutorial.items import NovelItem
from datetime import datetime
from bs4 import BeautifulSoup as bs

class QuotesSpider(scrapy.Spider):
    """docstring for QuotesSpider"""
    name = "quotes"
    start_urls = [
            'http://quotes.toscrape.com/tag/humor'
        ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span,text::text').extract_first(),
                'author': quote.xpath('span/small/text()').extract_first(),
            }
        next_page = response.css('li.next a::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)


class NovelSpider(scrapy.Spider):
    """docstring for NovelSpider"""
    name = "novelcrawler"
    #allowed_domains = "syosetu.com"
    start_urls = [
        # 'http://localhost:8842/Subpage/%E7%95%B0%E4%B8%96%E7%95%8C%E8%BF%B7%E5%AE%AE%E3%81%AE%E6%9C%80%E6%B7%B1%E9%83%A8%E3%82%92%E7%9B%AE%E6%8C%87%E3%81%9D%E3%81%86.html',
        'https://ncode.syosetu.com/n0089bk/'
    ]

    def parse(self, response):
        """ 爬虫主体 """
        Book = NovelItem()
        index = bs(response.body, 'lxml').find('div',class_ = 'index_box')
        href_info = response.xpath('//*[@id="head_nav"]/li[2]/a').attrib['href']
        Book['Index'] = self.part_index(index)
        Book = scrapy.Request(url=href_info,meta={'Item':Book}, callback=self.part_info)
        yield Book


    def part_info(self, response):
        """ 额外网页的info获取函数 """
        Book = response.meta['Item']
        Book['ncode'] = response.xpath('//*[@id="ncode"]').re(r'\w\d+\w+')[0]
        Book['Title'] = response.xpath('//*[@id="contents_main"]/h1/a').re(r'\w+')[-2]
        Book['Auther'] = response.xpath('//*[@id="noveltable1"]/tr[2]/td/a').re(r'>\S+</')[0][1:-2]
        Book['EX'] = response.xpath('//*[@id="noveltable1"]/tr[1]/td').get()[15:-5].replace('<br>','\n')
        if len(response.xpath('//*[@id="noveltype"]')) == 1:
            Book['State'] = '连载'
        else:
            Book['State'] = '完结'
        _t1 = response.xpath('//*[@id="noveltable2"]/tr[1]/td')
        Book['begindate'] = datetime.strptime(_t1.get(), '<td>%Y年 %m月%d日 %H時%M分</td>')
        _t2 = response.xpath('//*[@id="noveltable2"]/tr[2]/td')
        Book['update'] = datetime.strptime(_t2.get(), '<td>%Y年 %m月%d日 %H時%M分</td>')
        _tag = response.xpath('//*[@id="noveltable1"]/tr[3]/td')
        Book['Tag'] = set(_tag.re(r'(\w+)')) - set(('span','td'))
        _typed = response.xpath('//*[@id="noveltable1"]/tr[4]/td').re(r'(\w+)')
        Book['Type'] = (_typed[1],_typed[2])

        _re = response.xpath('//*[@id="noveltable2"]/tr[3]/td').re(r'[\d,]+')
        _re = _re + response.xpath('//*[@id="noveltable2"]/tr[4]/td').re(r'[\d,]+')
        _re = _re + response.xpath('//*[@id="noveltable2"]/tr[5]/td').re(r'[\d,]+')
        _re = _re + response.xpath('//*[@id="noveltable2"]/tr[6]/td').re(r'[\d,]+pt')
        _re = _re + response.xpath('//*[@id="noveltable2"]/tr[7]/td').re(r'([\d,]+pt)') # .replace(',','')
        Book['Hotpower'] = [x.replace(',','') for x in _re]
        _count = response.xpath('//*[@id="noveltable2"]/tr[10]/td').re(r'[\d,]+')
        Book['Count'] = _count[0]
        yield Book


    def part_index(self, index):
        """ 目录获取函数 """
        Book_index = []
        Chapter = ''
        sub_num = 1
        for sub in index.find_all(class_ = True,recursive=False):
            subox = {}
            if sub.attrs['class'][0] == 'chapter_title':
                Chapter = sub.text
                continue
            elif sub.attrs['class'][0] == 'novel_sublist2':
                t_update = sub.select('.long_update')[0].text.replace('\n','').replace('（改）','')
                _t1 = datetime.strptime(t_update,'%Y/%m/%d %H:%M')
                subox['Subnum'] = sub_num
                subox['Chapter'] = Chapter
                subox['Subtitle'] = sub.dd.a.text
                subox['Href'] = sub.dd.a.attrs['href']
                subox['Update'] = _t1
                if sub.select('.long_update')[0].span:
                    t_spandate = sub.select('.long_update')[0].span.attrs['title']
                    _t2 = datetime.strptime(t_spandate,'%Y/%m/%d %H:%M 改稿')
                    subox['Spandate'] = _t2
                else:
                    subox['Spandate'] = None
                sub_num += 1
            else:
                pass
            Book_index.append(subox)

        return Book_index

