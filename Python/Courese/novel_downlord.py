# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 23:34:55 2018

@author: z
"""

import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd
page = "https://ncode.syosetu.com"
novel_href = 'n1576cu'

#soup.head.link.attrs['href']

def get_index(page,href):
    
    index_page = rq.get(page + '/' + href)
    index_page.encoding = "utf-8"
    novel_soup = bs(index_page.text,'lxml')
    
    Book_Data = {}
    s = novel_soup.find(id = "novel_color")
    Book_Data['Title'] = s.find('p',class_ = "novel_title").text
    Book_Data['Auther'] = s.find('div',class_ = "novel_writername").a.text
    Book_Data['EX'] = s.find('div',id = "novel_ex").text
    index = s.find('div',class_ = 'index_box')
    Book_index = []
    Chapter = ''
    sub_num = 1
    for sub in index.findAll(class_ = True,recursive=False):
        subox = {}
        if sub.attrs['class'][0] == 'chapter_title':
            Chapter = sub.text
            continue
        elif sub.attrs['class'][0] == 'novel_sublist2':
            subox['Subnum'] = sub_num
            subox['Chapter'] = Chapter
            subox['Subtitle'] = sub.dd.a.text
            subox['Href'] = sub.dd.a.attrs['href']
            subox['Update'] = sub.select('.long_update')[0].text.replace('\n','').replace('（改）','')
            if sub.select('.long_update')[0].span:
                subox['Spandate'] = sub.select('.long_update')[0].span.attrs['title']
            sub_num += 1
        else:
            continue
        Book_index.append(subox)
    Book_index = pd.DataFrame(Book_index)
    Book_Data['Index'] = Book_index
    Book_Data['Text'] = get_text(page,Book_index)
    return Book_Data

def get_chapter(page,href):
    chapter = rq.get(page + '/' + href)
    chapter.encoding = "utf-8"
    chaptersoup = bs(chapter.text,'lxml')
    
    Chapter = {}
    Chapter['No'] = chaptersoup.find(id="novel_no").text
    Chapter['title'] = chaptersoup.find(class_='novel_subtitle').text
    Chapter['page'] = chaptersoup.find(id="novel_honbun")
    Chapter['note'] = chaptersoup.find(id="novel_a")
    
    return Chapter

def get_text(page,book_index):
    Book_Text = []
    for chap in book_index['Href']:
        print('download start:' + chap)
        Chapter = get_chapter(page,chap)
        Book_Text.append(Chapter)
        print('download compult.')
    Book_Text = pd.DataFrame(Book_Text)
    return Book_Text


Data = get_index(page,novel_href)