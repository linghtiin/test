# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 00:01:23 2018

@author: Linghtiin
@

区块链测试
"""

import json
import random
import string
import hashlib
import time

from threading import Thread
from decimal import Decimal


class Block(object):
    """
    区块类
        index:区块ID，依次递增
        hash:区块哈希
        previous_hash:上一区块哈希
        nonce:随机数
        difficulty:难度
        timestamp:时间戳
        type:区块类型（用于拓展协议）
        
        tip:标签
        transaction_data:区块体（暂定）
    """
    def __init__(self):
        self.index = None
        self.hash = None
        self.previous_hash = None
        self.nonce = None
        self.difficulty = None
        self.timestamp = None
        self.type = None
        
        self.tip = None
        self.transaction_data = None

    def get_block(self):
        """ 返回区块信息 """
        block = {
            'Index': self.index,
            'Hash': self.hash,
            'Previous_hash': self.previous_hash,
            'Nonce': self.nonce,
            'Difficulty': self.difficulty,
            'Timestamp': self.timestamp,
            'type': self.type,
            'tip': self.tip,
            'Transaction_data': self.transaction_data,
        }
        return block
    
    def get_block_header(self):
        """ 返回区块头 """
        block_header = {
            'Index': self.index,
            'Hash': self.hash,
            'Previous_hash': self.previous_hash,
            'Nonce': self.nonce,
            'Difficulty': self.difficulty,
            'Timestamp': self.timestamp,
            'type': self.type,
        }
        return block_header
    
    def get_block_info(self):
        """ 返回区块索引信息 """
        block_info = {
            'Index': self.index,
            'Timestamp': self.timestamp,
            'tip': self.tip,
            'Transaction_data': self.transaction_data,
        }
        return block_info


class Pitman(object):
    """ 矿工类 """
    def mine(self, index, previous_hash, transaction_data):
        """ 定义矿工的挖矿方法,参数为该区块的序号,之前的id,交易信息 """
        begin_time = time.time()

        block = Block()
        block.index = index
        block.previous_hash = previous_hash
        block.transaction_data = transaction_data
        block.timestamp = time.time()
        
        # 根据之前的id和交易信息生成这个区块的id和随机数, 还有困难系数
        block.difficulty, block.hash, block.nonce = self.gen_hash(previous_hash, transaction_data)

        end_time = time.time()
        spend_time = end_time - begin_time

        return block, spend_time

    @staticmethod
    def gen_hash(previous_hash, transaction_data):
        """！！！ 哈希函数（暂定） """
        # 随机数, 从1到99999随机
        nonce = random.randrange(1, 99999)

        difficulty = 0
        guess = str(previous_hash) + str(nonce) + transaction_data
        res = hashlib.sha256(guess.encode()).hexdigest()
        # while (int(res[-1]) % 2) != 0:
        while res[-1] != '0':
            difficulty += 1
            nonce += difficulty
            guess = previous_hash + str(nonce) + transaction_data
            res = hashlib.sha256(guess.encode()).hexdigest()

        return difficulty, res, nonce


class MyThread(Thread):
    """！！！ 自定义线程 """
    def __init__(self, target, args=()):
        super(MyThread, self).__init__()
        self.func = target
        self.arg = args
        self.result = None

    def run(self):
        self.result = self.func(*self.arg)

    def get_result(self):
        try:
            return self.result
        except Exception as e:
            print('自定义线程获取结果时发生了错误:', e)
            return None


class BlockChain(object):
    """ 区块链类 """
    def __init__(self, hash_num):
        self.chain_list = []
        self.gen_block(hash_num)

    @property
    def get_last_block(self):
        """ 获取最新区块（只读） """
        if len(self.chain_list):
            return self.chain_list[-1]
        return None

    def get_trans(self):
        """ 随机生成一份交易信息, 交易信息就是json字符串 """
        dict_data = {
            # random.sample可以从一个序列中随机获取指定数量的元素
            'sender': ''.join(random.sample(string.ascii_letters + string.digits, 8)),
            'recipient': ''.join(random.sample(string.ascii_letters + string.digits, 8)),
            # 相当于random.choice(range(1, 10000))
            'amount': random.randrange(1, 10000),
            }

        return json.dumps(dict_data)

    # 生成新区块的方法
    def gen_block(self, initial_hash=None):
        # 根据传参判断是否是创世区块

        # 如果是创世区块
        if initial_hash:
            # 先用区块类定义一个区块
            block = Block()
            # 然后对创建好的对象的实例属性进行设置
            block.index = 0
            block.nonce = random.randrange(0, 99999)
            block.previous_hash = '0'
            # 写到此, 我并不知道这个0是怎么来的, 以后是不是还要赋其他值?
            # 已经了解了, 0就是创世区块, 第一个, 所以是0

            block.difficulty = 0
            # 区块的交易信息
            block.transaction_data = self.get_trans()

            # 哈希值
            # guess = f'{block.previousHash}{block.nonce}{block.transactionData}'.encode()
            # 这个写法我没有看懂,
            # 看懂了, 是字符串格式化的另一种写法: f写法
            guess = str(block.index) + str(block.nonce) + block.previous_hash
            block.hash = hashlib.sha256(guess.encode()).hexdigest()

            block.timestamp = time.time()

            self.chain_list.append(block)

        # 如果不是创世区块
        else:
            # 先启动六个矿工开始挖矿
            for pitman in self.pitman_list:
            # for i in range(len(self.pitman_list)):
                # todo: 参数先不写, 以后在写
                t = MyThread(target=pitman.mine, args=(pitman,
                                                       len(self.chain_list),
                                                       # 获取当前这个区块链的最后一个区块的id
                                                       self.get_last_block.get_block_info()['Hash'],
                                                       # 获取交易信息
                                                       self.get_trans()))

                # t = MyThread(target=self.pitman_list[i].mine, )
                t.start()
                t.join()

                # 存储挖出来的区块
                self.result_list.append(t.get_result())

            print("All blocks generated by pitmen:")
            # 挖完了之后就该打印挖到的区块了
            # 上一个循环是同时启动六个矿工的线程开始运行, 等运行都完毕之后, 才开始继续主程序的运行, 是这样的吗?
            for result in self.result_list:
                print(result[0].get_block_info())

            # 获取新的区块
            # 先找到这个符合标准的区块

            # 先取出来第一个挖出来的区块
            first_block = self.result_list[0][0]
            # 再获取第一个区块计算耗费的时间, 转换成标准小数
            min_time = Decimal(self.result_list[0][1])

            # 去寻找那个用时最短的矿工挖出来的区块
            for i in range(1, len(self.result_list)):
                if Decimal(self.result_list[i][1]) < min_time:
                    first_block = self.result_list[i][0]

            # 找到以后存储
            self.chain_list.append(first_block)
            # 清空结果列表
            self.result_list = []

    def show_chain(self):
        for block in self.chain_list:
            print(block.get_block_info())


if __name__ == '__main__':
    chain = BlockChain(1)
    for i in range(20):
        chain.gen_block()
    chain.show_chain()
