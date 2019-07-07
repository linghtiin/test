# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 00:33:02 2019
    待办:
        check_index: 添加从数据库获取已有数据进行增量更新的功能

    预定规则：
        返回值[ -1:错误，需要重新加载；
                0：完成任务，结束运行；
                1：正常输出]
@author: 10127
"""
import json
from time import sleep as timesleep
from collections import OrderedDict
from httpclient import HttpClient
from htmlfilter import get_info, get_index, get_text

from sql_connect import My_sqlconnecter


class Noveldownloader(object):
    """docstring for Noveldownloader"""
    def __init__(self, ncode):
        super(Noveldownloader, self).__init__()
        self.home = "https://ncode.syosetu.com"
        self.ncode = ncode
        self.check = []
        self.Text = OrderedDict()
        self.info = None
        self.index = []
#        self.check_index()
#        self.run()
#        self.save()
        
    def check_index(self):
        """ 目录检查,更新check, """
        _urls = (self.home + "/novelview/infotop/ncode/" + self.ncode,
                 self.home + '/' + self.ncode)
        try:
            print('check index:')
            HClient = HttpClient(_urls)
            _pages = HClient.pages
        except:
            print('Error!!get page fail.')
            print('please tey again.')
            raise 
            return -1
        if None in _pages:
            print('get page fail.')
            print('please try again.')
            return -1
        
        _info = get_info(_pages[0])
        _index = get_index(_pages[1])
        
        
        mysql = My_sqlconnecter()
        _info_sql = mysql.read_info(self.ncode)
        _index_sql = mysql.read_index(self.ncode)
        mysql.disconnect()
        
        #检测数据库，是否为新书籍
        if (_info_sql == None) | (_index_sql == None):
            print("New Book:", _info[0]['ncode'], '\n\t', _info[0]['Title'])
            self.info = _info
            self.index = _index
            self.check = [False] * len(_index)
            return 2
        #检查数据更新时间,是否已完成下载
        if (_info_sql.UpDate == _info[0]['update']) & (len(_index) == len(_index_sql)):
            if all(map(lambda x: x.Check,_index_sql)):
                print('Book:',self.ncode,' has Downloaded complete.')
                self.info = _info_sql
                self.index = _index_sql
                self.check = list(map(lambda x: x.Check,_index_sql))
                return 0
        #逐个更新check
        self.check = []
        for i,v in enumerate(_index):
            if i < len(_index_sql):
                if len(v) == 5:
                    self.check.append(_index_sql[i].Check)
                elif (len(v) == 6) & (v['Spandate'] == _index_sql[i].Spandate):
                    self.check.append(_index_sql[i].Check)
                else:
                    self.check.append(False)
            else:
                self.check.append(False)
                
        self.info = _info
        self.index = _index
        return 1
    
    
    def run(self):
        """ 通过提交委托下载文本 """
        _urls = []
        for v in filter(lambda x: not self.check[x['Subnum']-1],self.index):
            _urls.append(self.home + v['Href'])
                
        try:
            print('run:')
            HClient = HttpClient(_urls)
            for x in HClient.page_generater():
                if x==0:
                    break
                elif x != None:
                    _text = get_text(x);
                    self.Text[_text['No']] = _text
                    self.check[int(_text['No'])-1] = True
        except:
            print('download text fail.')
            raise
            return -1
        HClient.close()    
        if all(self.check) == True:
            return 1
        else:
            return 0
    
    def save(self):
        """ 保存文件,不能转换datetime数据 """
        js = {'Info': self.info[0],
              'recoed': self.info[1],
              'Index': self.index,
              'Check': self.check,
              'Text': self.Text}
        with open('.\\' + self.ncode + '.json' ,'a') as f:
            f.write(json.dumps(js))
            
    def to_sql(self):
        """ 将数据储存至SQL数据库 """
        sql_con = My_sqlconnecter()
        sql_con._add_info(self.info[0])
        sql_con._add_index(self.index)
        sql_con.disconnect()
        
    def index_update_sql(self):
        """ 更新SQL数据库 """
        sql_con = My_sqlconnecter()
        sql_con.update_info(self.info[0])
        sql_con.update_index(self.index, self.ncode)
        sql_con.disconnect()
        
    def text_update_sql(self):
        """ 更新数据库内text """
        _text = []
        for chap in self.Text.values():
            _chap = chap.copy()
            _chap['Text'] = text_tran(chap['Text'])
            _text.append(_chap)
        sql_con = My_sqlconnecter()
        sql_con.update_text(_text)
        sql_con.disconnect()
        
        
def text_tran(Text):
    """ 行列表文本转换 """
    text = ""
    for line in Text.values():
        if line == "":
            text += '\n'
        else:
            text += line + '\n'
    return text
    
def text_intran(text):
    """ 行列表文本逆变换 """
    Text = {}
    for i, line in enumerate(text.split('\n')[0:-1]):
        Text['L'+str(i+1)] = line
    return Text
    
if __name__ == "__main__":
#    n1 = Noveldownloader('n0089bk')
#    n1.index_update_sql()
#    n1.run()
#    n1.text_update_sql()
    
    n2 = Noveldownloader('n4251cr')
    f = n2.check_index()
    if f == 0:
        pass
    elif f == 1:
        print('\t update the index.')
        n2.index_update_sql()
        while n2.run() :
            n2.text_update_sql()
            timesleep(20)
    elif f == 2:
        print('\t add the info&index.')
        n2.to_sql()
        while n2.run() :
            n2.text_update_sql()
            timesleep(20)
        
            