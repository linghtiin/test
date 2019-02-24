# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 18:53:12 2019

@author: z
"""

class Settings():
    """ 用于储存游戏设置的类。 """
    def __init__(self):
        """ 初始化游戏的设置 """
        
        #屏幕
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.fps_conf = 60
        
        #飞船
        self.ship_speed_factor = 1.5
        
        #子弹
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullet_allowed = 5
        
        
        
        
        
        
        
        
        