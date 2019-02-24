# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 20:24:01 2019

@author: z
"""

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """ 子弹类"""
    
    def __init__(self, ai_settings, screen, ship):
        """ 创建子弹 """
        super(Bullet, self).__init__()
        self.screen = screen
        
        #指定子弹坐标
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        
        #浮点位置
        self.y = float(self.rect.y)
        
        #子弹精灵
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor
        
    def update(self):
        """ 子弹状态更新 """
        self.y -= self.speed_factor
        self.rect.y = self.y
        
    def draw_bullet(self):
        """ 绘制子弹 """
        pygame.draw.rect(self.screen, self.color, self.rect)
    
    
    
    
    
    
    
    
    
    
    
    
    
    