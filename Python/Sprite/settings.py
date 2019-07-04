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
        self.ship_limit = 3
        
        #子弹
        self.bullet_width = 10
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullet_allowed = 4
        
        #外星人
        self.fleet_drop_speed =10
        self.alienpoints_scale = 1.5
        
        #游戏速度
        self.speedup_scale = 1.1
        
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        """  """
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
            #移动方向：fleet_direction, 1表示右移， -1表示左移
        self.fleet_direction = 1
        self.alien_points = 50
        
    def increase_speed(self):
        
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.alienpoints_scale)
        
        
        
        