# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 01:51:42 2018

@author: Linghtiin

钱包模块
"""

import json
import random
import string
import hashlib
import time
from threading import Thread
from decimal import Decimal

from BlockChain import BlockChain



class wellet(object):
    """ 钱包类 """
    def __init__(self):
        self.__account = None
        
    @property
    def blockchain(self,index = None):
        """ 读取区块链 """
        pass
    
    def updata(self):
        """ 数据更新 """
        pass
    
    def signature(self,msg,skey):
        """ 对消息进行签名 """
        pass
    
    def transaction(self,inpot,outpot,num):
        """ 发起交易 """
        pass