# -*- coding: utf-8 -*-
"""
Created on Fri May  3 13:28:01 2019
    待办：
        实现更新index、info函数
@author: 10127
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, UniqueConstraint
from sqlalchemy import Integer, Text, DateTime, Enum, Boolean
from sqlalchemy.orm import sessionmaker,exc
from sqlalchemy import create_engine

Base = declarative_base()

class Novel_info(Base):
    """ info表模型 """
    __tablename__ = 'novel_info'
    
    ncode = Column(Text, primary_key=True, unique=True, nullable=False)
    Title = Column(Text, unique=True, nullable=False)
    Auther = Column(Text)
    StartDate = Column(DateTime)
    EndDate = Column(DateTime)
    UpDate = Column(DateTime)
    State = Column(Enum('连载', '完结', '中止更新', '其它'))
       
    def __repr__(self):
        """ 查询输出格式 """
        return "<Novel_info(code={0} Title={1})>".format(self.ncode, self.Title)


class Novel_index(Base):
    """ index表模型 """
    __tablename__ = 'novel_index'
    
    ncode = Column(Text, primary_key=True, nullable=False)
    Subnum = Column(Integer, primary_key=True, nullable=False)
    Chapter = Column(Text)
    Subtitle = Column(Text)
    Update = Column(DateTime, nullable=False)
    Spandate = Column(DateTime)
    Href = Column(Text, unique=True, nullable=False)
    Check = Column(Boolean, nullable=False)
    Note = Column(Text)
    Text = Column(Text)
    
    __table_args__ = (
    UniqueConstraint('ncode', 'Subnum', name = 'uix_bookindex'),
    )
    
    def __repr__(self):
        """ 查询输出格式 """
        return "<Novel_index(code={0} Subnum={1} Title={2})>".format(self.ncode,self.Subnum, self.Subtitle)

    
    
class My_sqlconnecter():
    """ sql调用类 """
    def __init__(self):
        """ 初始化 """
        self.engine = create_engine(
                "mysql+mysqlconnector://own_py:123456@localhost:3306/test1?charset=utf8", 
                max_overflow=5)
        self._Session = sessionmaker(bind=self.engine) # 指定引擎
        self.session = self._Session()
        self.ncode = None
        self.state = 3
        
    def disconnect(self):
        """ 关闭连接 """
        self.session.close()
        self.engine.dispose()
        
        
    def _add_info(self,info):
        """ 添加info """

        if info['State'] == 0:
            _state = '连载'
            _enddate = None
        elif info['State'] == 1:
            _state = '完结'
            _enddate = info['update']
        elif info['State'] == 2:
            _state = '中止更新'
            _enddate = info['update']
        elif info['State'] == 3:
            _state = '其他'
            _enddate = info['update']
            
        self.ncode = info['ncode']
        self.state = _state
        temp = Novel_info(ncode= info['ncode'],
                          Title= info['Title'],
                          Auther= info['Auther'],
                          StartDate= info['begindate'],
                          EndDate=_enddate,
                          UpDate= info['update'],
                          State = _state)
        self.session.add(temp)
        try:
            self.session.commit()
        except:
            self.session.rollback()
            self.disconnect()
            raise
    
    
    def _add_index(self,index):
        """ 添加index """
        for line in index:
            if 'Spandate' not in line.keys():
                _spandate = None
            else:
                _spandate = line['Spandate']
            temp = Novel_index(ncode=self.ncode,
                               Subnum=line['Subnum'],
                               Chapter=line['Chapter'],
                               Subtitle=line['Subtitle'],
                               Update=line['Update'],
                               Spandate=_spandate,
                               Href=line['Href'],
                               Check=False)
            self.session.add(temp)
            
        try:
            self.session.commit()
        except:
            self.session.rollback()
            self.disconnect()
            raise
            
        
    def _add_text(self,text):
        """ 添加text """
        temp = {'Check': True,
                'Text': text['Text'],
                'Note': text['note']}
        self.session.query(Novel_index).filter(     \
                                          Novel_index.ncode == text['ncode'],
                                          Novel_index.Subnum == text['No'],
                                          ).update(temp)
        try:
            self.session.commit()
        except:
            self.session.rollback()
            self.disconnect()
            raise
        
        
    def read_info(self, ncode):
        """ 获取书籍更新时间 """
        return self.session.query(Novel_info).filter(Novel_info.ncode == ncode).one()
    
    def read_index(self, ncode):
        """ 获取目录更新时间 """
        return self.session.query(Novel_index).filter(Novel_index.ncode == ncode).all()
    
    
    def update_info(self, info):
        """ 更新info """
        _org_info = self.session.query(Novel_info).filter(Novel_info.ncode == info['ncode'])
        if info['State'] != _org_info.one().State:
            temp = {'State':info['State'],
                    'EndDate':info['update']}
            _org_info.update(temp)        
        try:
            self.session.commit()
        except:
            self.session.rollback()
            self.disconnect()
            raise
            
    
    def update_index(self, index, ncode):
        """ 更新index """
        for line in index:
            _org_line = self.session.query(Novel_index).filter(     \
                                          Novel_index.ncode == ncode,
                                          Novel_index.Subnum == line['Subnum'])
            try:
                _org_line_one = _org_line.one_or_none()
            except exc.MultipleResultsFound as e:
                print('Multiple Results has Found.')
                raise e
                    
            if _org_line_one == None:
                print('Subnum:',line['Subnum'],'\tby Add.')
                if 'Spandate' not in line.keys():
                    _spandate = None
                else:
                    _spandate = line['Spandate']
                temp = Novel_index(ncode=ncode,
                           Subnum=line['Subnum'],
                           Chapter=line['Chapter'],
                           Subtitle=line['Subtitle'],
                           Update=line['Update'],
                           Spandate=_spandate,
                           Href=line['Href'],
                           Check=False)
                self.session.add(temp)
                
            elif 'Spandate' in line.keys():                    
                if _org_line_one.Spandate == None:
                    print('Subnum:',line['Subnum'],'\tby has Span.')
                    temp = {'Spandate': line['Spandate'],
                            'Check': False,
                            'Text': None,
                            'Note': None}
                    _org_line.update(temp)
                elif line['Spandate'] > _org_line_one.Spandate :
                        print('Subnum:',line['Subnum'],'\tby newer Span.')
                        temp = {'Spandate': line['Spandate'],
                                'Check': False,
                                'Text': None,
                                'Note': None}
                        _org_line.update(temp)
                    
        try:
            self.session.commit()
        except:
            self.session.rollback()
            self.disconnect()
            raise


    def update_text(self,tests):
        """ 批量更新text """
        print(tests[0]['ncode'])
        for line in tests:
            _org_line = self.session.query(Novel_index).filter(     \
                                                Novel_index.ncode == line['ncode'],
                                                Novel_index.Subnum == int(line['No']))
            try:
                _org_line_one = _org_line.one_or_none()
            except exc.MultipleResultsFound as e:
                print('Multiple Results has Found.')
                raise e
                    
            if _org_line_one == None:
                print('line',line['No'],'not found.')
                
            elif _org_line_one.Check == False:
                print('line', line['No'])
                temp = {'Check': True,
                        'Text': line['Text'],
                        'Note': line['note']}
                _org_line.update(temp)
        try:
            self.session.commit()
        except:
            self.session.rollback()
            self.disconnect()
            raise
            
            
if __name__ == '__main__':
    
    my_con = My_sqlconnecter()
    
    infotime = my_con.read_info('n0089bk')
    indextime = my_con.read_index('n0089bk')
    
#    my_con._add_info(box['info'][0][0])
#    my_con._add_index(box['index'][1])
#    
#    my_con._add_info(box['info'][2][0])
#    my_con._add_index(box['index'][1])
#
#    my_con._add_info(box['info'][3][0])
#    my_con._add_index(box['index'][1])
    
#    my_con._add_text(box['text'][0])
    my_con.disconnect()
    

















