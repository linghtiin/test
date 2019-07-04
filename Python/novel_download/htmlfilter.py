# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 23:08:45 2019
    待办：
        get_info:temp字典格式化
    
@author: 10127
"""
from datetime import datetime
#from bs4 import element as em
from bs4 import BeautifulSoup as bs

def get_info(page):
    """ 从info网页中提取基本书籍信息 """
    page_soup = bs(page,'lxml')
    s = page_soup.find('div',id = "contents_main")
    t1 = s.find('table',id='noveltable1')
    t2 = s.find('table',id='noveltable2')

    Book_Info = {}
    Book_Info['ncode'] = s.find('p', id='ncode').text
    Book_Info['Title'] = s.h1.a.text    
    
    if s.find('div',id='pre_info').span['id'] == 'noveltype_notend':
        Book_Info['State'] = '连载'
    elif s.find('div',id='pre_info').span['id'] == 'noveltype':
        Book_Info['State'] = '完结'
    else:
        Book_Info['State'] = '其它'
        
    temp = {}
    for tr in t1.find_all('tr'):
        temp[tr.th.text] = tr.td.text
    for tr in t2.find_all('tr'):
        temp[tr.th.text] = tr.td.text.split('※')[0]
        
    _t1 = datetime.strptime(temp['掲載日'],'%Y年 %m月%d日 %H時%M分')
    # Book_Info['Auther'] = s.find('div',class_ = "novel_writername").a.text
    # Book_Info['EX'] = s.find('div',id = "novel_ex").text        
    Book_Info['Auther'] = temp['作者名']
    Book_Info['EX'] = temp['あらすじ']
    Book_Info['begindate'] = _t1
    if Book_Info['State'] == '完结':
        _t2 = datetime.strptime(temp['最終部分掲載日'],'%Y年 %m月%d日 %H時%M分')
        Book_Info['update'] = _t2
    else:
        _t2 = datetime.strptime(temp['最新部分掲載日'],'%Y年 %m月%d日 %H時%M分')
        Book_Info['update'] = _t2
        
    return Book_Info, temp


def get_index(page):
    """ 从index网页中提取书籍目录 """
    page_soup = bs(page,'lxml')
    index = page_soup.find('div',class_ = 'index_box')
    
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
            sub_num += 1
        else:
            pass
        Book_index.append(subox)
    return Book_index

def get_text(page):
    """ 从正文网页中提取文章 """
    page_soup = bs(page,'lxml')
    h = page_soup.find('ul', id = "head_nav").find_all('li')
    t = page_soup.find('div', class_ = "contents1")
    s = page_soup.find('div', id = "novel_color")
    
    Chapter = {}
    Chapter['ncode'] = h[1].a.attrs['href'].split('/')[-2]
    Chapter['chapter_title'] = t.find('p', class_ = "chapter_title").text
    
    Chapter['No'] = s.find('div', id = "novel_no").text.split('/')[0]
    Chapter['subtitle'] = s.find('p', class_ = 'novel_subtitle').text
    
    Chapter['Text'] = _str_chapter(s.find('div', id = "novel_honbun"))
    
    if s.find('div', id="novel_a") == None:
        Chapter['note'] = None
    else:
        Chapter['note'] = s.find('div', id = "novel_a").text
    return Chapter

def _str_chapter(tag):
    """ 文本格式化 """
    text = {}
    for line in tag.find_all('p', id = True):
        text[line.attrs['id']] = line.text.replace('\u3000', '\t')
    return text



if __name__ == '__main__':
    
    ty = ['text','index','text','text','index','info','text','text','index','info','index','info']
    box = {'info':[],'index':[],'text':[]}
    for i,t in enumerate(ty):
        if t == 'info':
            box[t].append(get_info(ps[i]))
        elif t == 'index':
            box[t].append(get_index(ps[i]))            
        elif t == 'text':
            box[t].append(get_text(ps[i]))    
    del i,t,ty
    
#    info1,temp1 = get_info(page1)
    