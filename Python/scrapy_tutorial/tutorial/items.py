# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.org/en/latest/topics/items.html

from scrapy import Item, Field


class TutorialItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class Novelshort(Item):
    """docstring for NovelItem"""
    ncode = Field()
    Title = Field()
    Auther = Field()
    State = Field()

    # 时间数据
    StartDate = Field()
    EndDate = Field()
    UpDate = Field()
    
class NovelItem(Item):
    """item for NovelInfo"""
    # collection = table = NovelInfo
    ncode = Field()
    Title = Field()
    Auther = Field()
    EX = Field()

    Index = Field()
    Text = Field()

    State = Field()
    begindate = Field()
    update = Field()
    Tag = Field()
    Type = Field()
    Hotpower = Field()
    Count = Field()
        