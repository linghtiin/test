# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import datetime

class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlPipeline(object):
    """docstring for SQLPipeline"""
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, 
                                    self.user, 
                                    self.password, 
                                    self.database, 
                                    port=self.port, 
                                    charset='utf8')
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()

    def process_item(self, item, spider):
        """ add item """
        ins1 = """INSERT INTO `test1`.`book` 
                    (`ncode`, `Title`, `Auther`, `State`, `begindate`, `update`, `EX`, `Tag`, `Type`, `Hotpower`, `Count`) 
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
        data1 = (item['ncode'], item['Title'], item['Auther'], item['State'],
                item['begindate'].strftime('%Y-%m-%d %H:%M:%S'),
                item['update'].strftime('%Y-%m-%d %H:%M:%S'), 
                item['EX'], str(item['Tag']), str(item['Type']), str(item['Hotpower']),
                item['Count'])
        
        ins2 = """INSERT INTO `test1`.`bookcontent` 
                (`ncode`, `Subnum`, `Chapter`, `Subtitle`, `update`, `spandate`) 
                VALUES (%s, %s, %s, %s, %s, %s);"""
        
        self.cursor.executemany(ins1, [data1])
        data2_sum = []
        for i in range(len(item['Index'])):
            data2 = (item['ncode'], item['Index'][i]['Subnum'], 
                item['Index'][i]['Chapter'], item['Index'][i]['Subtitle'], 
                item['Index'][i]['update'], item['Index'][i]['spandate'])
            data2_sum.append(data2)
        self.cursor.executemany(ins2, data2_sum)
        self.db.commit()

        return item

        # data = dict(item)
        # keys = ', '.join(data.keys())
        # values = ', '.join(['%s'] * len(data))
        # sql = 'insert into %s (%s) values (%s)' % (item['table'], keys, values)
        # self.cursor.execute(sql, tuple(data.values()))
        # self.db.commit()
        # return item
        