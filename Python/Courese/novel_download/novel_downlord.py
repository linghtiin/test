# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 23:34:55 2018

@author: z
"""

import os
import bs4
import time
import json
import random
import numpy as np
import pandas as pd
import requests as rq
from bs4 import BeautifulSoup as bs


#soup.head.link.attrs['href']
###############################################################################

def check_book_index(workpath, page_href, novel_code, header):
    """ 保存书籍。并根据信息下载章节文本。（未完成） """

    novelpath = create_folder(workpath, novel_code)
    PageSoup = get_PageSoup(page_href, novel_code, header)

    Book_Info = create_book_info(PageSoup)
    Book_index = create_book_index(PageSoup)
    
    #保存书籍信息
    save_info(novelpath, Book_Info)

    #检查已下载目录
    excelpath = novelpath + '\\' + novel_code + '.xlsx'
    Book_index = save_index(excelpath, Book_index)
    
    flag = Book_index['Downloaded'].all()
    if not flag:
        return novel_code
    
    return None

def create_folder(workpath, novel_code):
    """ 创建文件夹，返回文件储存路径 """
    try:
        os.mkdir(novel_code)
    except WindowsError as e:
        print('Error!!文件夹已存在。')
        print(e)
    finally:
        print('创建文件夹完成。')
    novelpath = workpath + '\\' + novel_code
    return novelpath

def get_PageSoup(page_href, pathref, header):
    """ 根据网站与目录路径获取网页Soup """
    
    if header == None:
        header = {'user-agent': None}    
        
    trydo = 10
	#获取网页，捕获错误+验证状态码
    while True:                
        try:
            Page = rq.get(page_href + '/' + pathref,headers=header,timeout = (30,30))
        except rq.exceptions.ConnectTimeout as e :
            print('ConnectTimeout!!\n\tError code:' + str(e.errno))
            error_download(e)
            print('Well be waiting 5 min to try again.')
            time.sleep(5*60)
            return None
        except rq.exceptions.ReadTimeout as e :
            print('ReadTimeout!!\n\tError code:' + str(e.errno))
            error_download(e)
            print('Well be waiting 5 min to try again.')
            time.sleep(5*60)
        except :
            print('Unknow Error!!!')
            print('Will stop download.')
            raise
        
        if Page.status_code == rq.codes.ok:
            Page.encoding = "utf-8"
            PageSoup = bs(Page.text,'lxml')
            break
        else:
            trydo -= 1
            if trydo <= 0:
                print('status code error!!\n\tcode is ' + str(Page.status_code))
                print('Will be stop download.')
                Page.raise_for_status()
            print('status code error!!')
            print('Will be try again.')
            time.sleep(10)
		
    return PageSoup

def create_book_info(novel_soup):
    """ 从网页中提取基本书籍信息 """
    s = novel_soup.find(id = "novel_color")
    Book_Info = {}
    Book_Info['Title'] = s.find('p',class_ = "novel_title").text
    Book_Info['Auther'] = s.find('div',class_ = "novel_writername").a.text
    Book_Info['EX'] = s.find('div',id = "novel_ex").text
    Book_Info['update'] = ''
    Book_Info['begindate'] = ''
    return Book_Info

def create_book_index(novel_soup):
    """ 从网页中提取书籍目录 """
    index = novel_soup.find('div',class_ = 'index_box')
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
            pass
        Book_index.append(subox)
    return pd.DataFrame(Book_index)

def save_info(novelpath, Book_Info):
    """ 保存书籍信息 """
    with open(novelpath + '\\Info.txt','w') as f:
        f.write(json.dumps(Book_Info))
    
def save_index(excelpath, Book_index):
    """ 保存、更新小说目录 """
    
    Book_index['Downloaded'] = np.zeros(len(Book_index),dtype=int)
    Book_index['Note'] = None       #未测试的代码
    try:
        temp_index = pd.read_excel(excelpath,'Index')
    except FileNotFoundError :      #文件未创建
        print('There hasn`t excel file.')
        excelwriter = pd.ExcelWriter(excelpath)
        Book_index.to_excel(excelwriter,'Index',na_rep= 'N/A')
        excelwriter.save()
        return Book_index

    #书籍目录有更新
    # for i in Book_index.index:
        # if Book_index.loc[i,'Spandate'] == temp_index.loc[i,'Spandate']:
            # Book_index.loc[i,'Downloaded'] = 1
        # else:
            # pass
      
    excelwriter = pd.ExcelWriter(excelpath)
    Book_index.to_excel(excelwriter,'Index',na_rep= 'N/A')
    excelwriter.save()
    return Book_index

###############################################################################

def create_chapter(novel_soup):
    """ 获取章节文本。 """
    
    s = novel_soup.find(id="novel_color")
    Chapter = {}
    Chapter['No'] = s.find(id="novel_no").text.split('/')[0]
    Chapter['subtitle'] = s.find(class_='novel_subtitle').text
    Chapter['chapter_title'] = novel_soup.find(class_="chapter_title")
    Chapter['Text'] = str_chapter(s.find(id="novel_honbun"))
    
    if s.find(id="novel_a") == None:
        Chapter['note'] = None
    else:
        Chapter['note'] = s.find(id="novel_a").text
    return Chapter
    
def str_chapter(soupText):
    """ 章节文本序列化处理，段落划分 """
    Text = []
    for Len in soupText.children:
        if type(Len) == bs4.element.Tag:
            if Len.find("br") == bs4.element.Tag:
                Text.append("\n")
            else:
                Text.append(Len.text)
    return pd.Series(Text)
        

###############################################################################
    
def download_text(page_href, Indexpath, header):
    """ 文本下载，存储到Excel文件，更新index。 """
    #读取书籍目录
    Book_index = pd.read_excel(Indexpath, 'Index')
    #检测已下载章节
    if len(Book_index[Book_index['Downloaded'] == 1]):
        Text = pd.read_excel(Indexpath, 'Text')
    else:
        Text = pd.DataFrame()
    #遍历未下载章节
    for i in Book_index[Book_index['Downloaded'] == 0].Subnum:
        Chapter = create_chapter(get_PageSoup(page_href, Book_index.at[i-1,'Href'], header))
        excelwriter = pd.ExcelWriter(Indexpath)
        if Chapter != None:
            Text[Chapter['No']] = Chapter['Text']
            Book_index.at[i-1,'Note'] = Chapter['note']
            Book_index.at[i-1,'Downloaded'] = 1
            Text.to_excel(excelwriter,sheet_name='Text')
            Book_index.to_excel(excelwriter,'Index',na_rep= 'N/A')
        else:
            return 1
        print('Downloaded %d.\n' % (i))
        excelwriter.save()
        time.sleep(random.random()*4 + 2)
    return 0        #完成下载，跳出循环

def error_download(e):
    pass
    

if __name__ == "__main__":

    workpath = os.getcwd()
    headers = {'user-agent': 'my-readapp/0.1'}
    page_href = "https://ncode.syosetu.com"
    novel_code = 'n9669bk'

    temp_href = '/n9669bk/1/'
	#下载、更新书籍目录
    # undownloadlist = check_book_index(workpath, page_href, novel_code, headers)
    undownloadlist = True
	#根据目录下载文本
    if undownloadlist:
        Indexpath = workpath + '\\' + novel_code + '\\' + novel_code + '.xlsx'
        download_text(page_href, Indexpath, headers)


