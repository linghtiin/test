"""
    测试案例爬虫
    TODO:

"""

#import re
import scrapy
import logging
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from tutorial.items import NovelItem
from datetime import datetime
from bs4 import BeautifulSoup as bs

logger = logging.getLogger('mycustomLogger')

class QuotesSpider(scrapy.Spider):
    """docstring for QuotesSpider"""
    name = "quotes"
    allowed_domains = ""
    start_urls = [
            'http://quotes.toscrape.com/tag/humor'
        ]
    my_tag_urls = set()
    my_used_urls = set()


    def start_requests(self):
        return [scrapy.FormRequest("http://quotes.toscrape.com/login",
                               formdata={'username': 'Linghtiin', 'password': '123456'},
                               callback=self.logged_in)]

    def logged_in(self, response):
        # here you would extract links to follow and return Requests for
        # each of them, with another callback
        # scrapy.shell.inspect_response(response, self)
        tags = response.xpath('/html/body/div/div[2]/div[2]/span')
        for tag in tags:
            shorthref = tag.xpath("./a/@href").get()
            taghref = response.urljoin(shorthref)
            self.my_tag_urls.add(taghref)
        nexttag = self.my_tag_urls.pop()
        self.my_used_urls.add(nexttag)
        return scrapy.Request(nexttag)


    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span,text::text').extract_first(),
                'author': quote.xpath('span/small/text()').extract_first(),
            }
        next_page = response.css('li.next a::attr("href")').extract_first()

        tags = response.css('a[class=tag]::attr("href")')
        for tag in tags:
            shorthref = tag.get()
            taghref = response.urljoin(shorthref)
            if taghref not in self.my_used_urls:
                self.my_tag_urls.add(taghref)
        if next_page is not None:
            yield response.follow(next_page, self.parse)
        elif len(self.my_tag_urls):
            nexttag = self.my_tag_urls.pop()
            self.my_used_urls.add(nexttag)
            logger.info('Tag`s len: %s' % (len(self.my_tag_urls)))
            yield response.follow(nexttag)
        else:
            scrapy.shell.inspect_response(response, self)
            return None


class NovelSpider(CrawlSpider):
    """docstring for NovelSpider"""
    name = "novelcrawler"
    allowed_domains = "syosetu.com"
    start_urls = [
        'https://ncode.syosetu.com/n0089bk/',
        'https://ncode.syosetu.com/n4251cr/'
    ]

    rules = (
        # info
        Rule(LinkExtractor(allow=('n0089bk/', ), deny=(r'\w+/', ))),
        Rule(LinkExtractor(allow=(r'\w+/', )), callback='parse_text')
        )

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
        Book['Count'] = _count[0].replace(',','')
        return Book


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
                subox['update'] = _t1
                if sub.select('.long_update')[0].span:
                    t_spandate = sub.select('.long_update')[0].span.attrs['title']
                    _t2 = datetime.strptime(t_spandate,'%Y/%m/%d %H:%M 改稿')
                    subox['spandate'] = _t2
                else:
                    subox['spandate'] = None
                sub_num += 1
            else:
                pass
            Book_index.append(subox)

        return Book_index

    def parse_text(self, response):
        """ get the text """
        pass

