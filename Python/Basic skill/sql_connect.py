# -*- coding: utf-8 -*-
"""
Created on Fri May  3 13:28:01 2019

@author: 10127
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, UniqueConstraint, Index
from sqlalchemy import Integer, Text, DateTime, Enum, Boolean
from sqlalchemy.orm import sessionmaker
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
    Update = Column(DateTime, unique=True, nullable=False)
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
        _t1 = '{0}-{1}-{2} {3}:{4}:{5}'.format(
                info['update'][0:4],
                info['update'][6:8],
                info['update'][9:11],
                info['update'][13:15],
                info['update'][16:18],
                '00')
        _t2 = '{0}-{1}-{2} {3}:{4}:{5}'.format(
                info['begindate'][0:4],
                info['begindate'][6:8],
                info['begindate'][9:11],
                info['begindate'][13:15],
                info['begindate'][16:18],
                '00')
        if info['State'] == 0:
            _state = '连载'
            _enddate = None
        elif info['State'] == 1:
            _state = '完结'
            _enddate = _t1
        elif info['State'] == 2:
            _state = '中止更新'
            _enddate = _t1
        elif info['State'] == 3:
            _state = '其他'
            _enddate = _t1
            
        self.ncode = info['ncode']
        self.state = _state
        temp = Novel_info(ncode= info['ncode'],
                          Title= info['Title'],
                          Auther= info['Auther'],
                          StartDate= _t2,
                          EndDate=_enddate,
                          UpDate= _t1,
                          State = _state)
        self.session.add(temp)
        try:
            self.session.commit()
        except:
            self.session.rollback()
            self.disconnect()
            raise
    
    
    def _add_index(self,indexs):
        """ 添加index """
        for index in indexs:
            _t1 = '{0}-{1}-{2} {3}:{4}:{5}'.format(
                    index['Update'][0:4],
                    index['Update'][5:7],
                    index['Update'][8:10],
                    index['Update'][11:13],
                    index['Update'][14:16],
                    '00')

            if 'Spandate' not in index.keys():
                _spandate = None
            else:
                _spandate = '{0}-{1}-{2} {3}:{4}:{5}'.format(
                    index['Spandate'][0:4],
                    index['Spandate'][5:7],
                    index['Spandate'][8:10],
                    index['Spandate'][11:13],
                    index['Spandate'][14:16],
                    '00')
            
            temp = Novel_index(ncode=self.ncode,
                               Subnum=index['Subnum'],
                               Chapter=index['Chapter'],
                               Subtitle=index['Subtitle'],
                               Update=_t1,
                               Spandate=_spandate,
                               Href=index['Href'],
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
        
    


if __name__ == '__main__':
    
    my_con = My_sqlconnecter()
    
    my_con._add_info(box['info'][0][0])
    my_con._add_index(box['index'][1])
    
    my_con._add_info(box['info'][2][0])
    my_con._add_index(box['index'][1])

    my_con._add_info(box['info'][3][0])
    my_con._add_index(box['index'][1])
    
#    my_con._add_text(box['text'][0])
    my_con.disconnect()
    











# 未验证代码
# 一对多
class Favor(Base):
    __tablename__ = 'favor'
    nid = Column(Integer, primary_key=True)
    caption = Column(String(50), default='red', unique=True) # 默认值、唯一索引

    def __repr__(self):
        return "%s-%s" %(self.nid, self.caption)

class Person(Base):
    __tablename__ = 'person'
    nid = Column(Integer, primary_key=True)
    name = Column(String(32), index=True, nullable=True)
    favor_id = Column(Integer, ForeignKey("favor.nid"))
    # 与生成表结构无关，仅用于查询方便
    favor = relationship("Favor", backref='pers')

# 多对多
class ServerToGroup(Base):
    # 关系表要放对应表上面，否则找不到
    __tablename__ = 'servertogroup'
    nid = Column(Integer, primary_key=True, autoincrement=True)
    server_id = Column(Integer, ForeignKey('server.id'))    # 外键
    group_id = Column(Integer, ForeignKey('group.id'))

    group = relationship("Group", backref='s2g')
    server = relationship("Server", backref='s2g')

class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False) # 不能为空
    port = Column(Integer, default=22)
    # group = relationship('Group',secondary=ServerToGroup,backref='host_list')


class Server(Base):
    __tablename__ = 'server'

    id = Column(Integer, primary_key=True, autoincrement=True) # 自增
    hostname = Column(String(64), unique=True, nullable=False)



def init_db():
    # 创建表
    Base.metadata.create_all(engine)

def drop_db():
    # 删除表
    Base.metadata.drop_all(engine)




