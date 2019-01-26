# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 23:34:55 2018

@author: z
"""

import os
import time
import json
import random
import numpy as np
import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd


#soup.head.link.attrs['href']

def get_index(page,href):
    """ 获取书籍基本信息，目录表。 """
    index_page = rq.get(page + '/' + href,headers=headers,timeout = (5,30))
    if index_page.status_code == rq.codes.ok:
        index_page.encoding = "utf-8"
        novel_soup = bs(index_page.text,'lxml')
    else:
        index_page.raise_for_status()

    s = novel_soup.find(id = "novel_color")
    Book_Data = {}
    Book_Data['Title'] = s.find('p',class_ = "novel_title").text
    Book_Data['Auther'] = s.find('div',class_ = "novel_writername").a.text
    Book_Data['href'] = href
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
    return Book_Data,Book_index

def get_chapter(page,href):
    """ 获取章节文本。 """
    trydo = 10
    while 1:                #网页交互，验证状态码+超时处理
        try:
            chapter = rq.get(page + '/' + href,headers=headers,timeout = (30,30))
        except rq.exceptions.ConnectTimeout as e :
            print('ConnectTimeout!!\n\tError code:' + str(e.errno))
            print('Save the downloaded text.')
            error_download()
            print('Well be waiting 5 min to try again.')
            time.sleep(5*60)
            return None
        except rq.exceptions.ReadTimeout as e :
            print('ReadTimeout!!\n\tError code:' + str(e.errno))
            print('Save the downloaded text.')
            error_download()
            print('Well be waiting 5 min to try again.')
            time.sleep(5*60)
            
        
        if chapter.status_code == rq.codes.ok:
            chapter.encoding = "utf-8"
            chaptersoup = bs(chapter.text,'lxml')
            break
        else:
            trydo -= 1
            if trydo <= 0:
                print('status code error!!\n\tcode is ' + str(chapter.status_code))
                chapter.raise_for_status()
            time.sleep(5)
    
    Chapter = {}
    Chapter['No'] = chaptersoup.find(id="novel_no").text.split('/')[0]
    Chapter['title'] = chaptersoup.find(class_='novel_subtitle').text
    Chapter['page'] = chaptersoup.find(id="novel_honbun").text
    Chapter['page'] = pd.Series(Chapter['page'].strip().split('\n\n\n'))
    Chapter['page'].loc[0] = Chapter['page'].loc[0] + '\t' + str(Chapter['title'])
    
    if chaptersoup.find(id="novel_a") == None:
        Chapter['note'] = None
    else:
        Chapter['note'] = chaptersoup.find(id="novel_a").text
    return Chapter

def save_book(workpath,page,novel_href):
    """ 保存书籍。并根据信息下载章节文本。（未完成） """
    try:
        os.mkdir(novel_href)
    except WindowsError as e:
        print('文件夹已创建。')
        print(e)
        
    novelpath = workpath + "\\" + novel_href
    Book_Info,Book_index = get_index(page,novel_href)
    #保存书籍信息
    with open(novelpath + r'\Info.txt','w') as f:
        f.write(json.dumps(Book_Info))
    
    #检查已下载目录
    excelpath = novelpath + r'\Index.xlsx'
    try:
        temp_index = pd.read_excel(excelpath,'Index')
        f = (Book_index['Update'] == temp_index['Update']).all() 
        f = f & (Book_index['Subnum'] == temp_index['Subnum']).all()
        if not f :
            excelwriter = pd.ExcelWriter(excelpath)
            Book_index['Downloaded'] = np.zeros(len(Book_index),dtype=int)
            Book_index.to_excel(excelwriter,'Index',na_rep= 'N/A')
            excelwriter.save()
            Text = pd.DataFrame()
        else:
            Book_index = temp_index
            Text = pd.read_excel(excelpath,'Text')
    except FileNotFoundError as e:
        print('there hasn`t excel file.')
        print(e)
        excelwriter = pd.ExcelWriter(excelpath)
        Book_index['Downloaded'] = np.zeros(len(Book_index),dtype=int)
        Book_index.to_excel(excelwriter,'Index',na_rep= 'N/A')
        excelwriter.save()
        Text = pd.DataFrame()

        
    #保存文本，断点续传
    while download_text(Book_index,Text,excelpath):
        excelwriter.save()
 
def download_text(Book_index,Text,excelpath):
    """ 文本下载，存储到Excel文件，更新index。 """
    Book_index['Note'] = None
    for i in Book_index[Book_index['Downloaded'] == 0].Subnum:
        Chapter = get_chapter(page,Book_index.at[i-1,'Href'])
        excelwriter = pd.ExcelWriter(excelpath)
        if Chapter != None:
            chap = Chapter['page']
            Text[Chapter['No']] = chap
            note = Chapter['note']
            Book_index.at[i-1,'Note'] = note
            Book_index.at[i-1,'Downloaded'] = 1
            Text.to_excel(excelwriter,sheet_name='Text')
            Book_index.to_excel(excelwriter,'Index',na_rep= 'N/A')
        else:
            return 1
        print('Downloaded %d.\n' % (i))
        excelwriter.save()
        time.sleep(random.random()*4 + 2)
    return 0        #完成下载，跳出循环

def error_download():
    pass
    
workpath = os.getcwd()
headers = {'user-agent': 'my-readapp/0.1'}
page = "https://ncode.syosetu.com"
novel_href = 'n1576cu'

save_book(workpath,page,novel_href)

#    excelreader = pd.ExcelFile(novelpath + r'\Index.xlsx')
#    with pd.read_excel(excelreader,'Index') as exc:
#        Book_index = exc   
    #保存文本,非格式化
#    with open(novelpath + r'\Info.txt','w') as f:
#        f.write(Book_Info['Title'])
#        f.write('\n\n')
#        f.write('作者：' + Book_Info['Auther'])
#        f.write('\n\n')
#        f.write(Book_Info['EX'])
#        f.write('\n\n\n\n\n')
#    for i in book_index.index:
#        Chapter = get_chapter(page,Book_index.Href[i])
#        with open(novelpath + r'\Info.txt','a') as f:
#            f.write(jso)
#            f.write('\n\n\n\n')
