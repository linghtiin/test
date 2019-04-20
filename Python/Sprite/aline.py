# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 22:34:41 2019

@author: z
"""
import pygame
from pygame.sprite import Sprite


class Aline(Sprite):
    """ 外星敌人类 """
    def __init__(self, ai_settings, screen):
        super(Aline, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        #加载图像
        self.image = pygame.image.load(r".\image\Ailne_1.png")
        self.rect = self.image.get_rect()
        #self.rect = pygame.Rect(0, 0, 20, 20)
        
        #初始化位置
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #浮点位置
        self.x = float(self.rect.x)
        
    def blitme(self):
        """ 外星人绘制 """
        self.screen.blit(self.screen, self.rect)
#        pygame.draw.rect(self.screen, (255, 0, 0), self.rect)
        
        
    def update(self):
        """ 外星人左右移动 """
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x
        
    def check_edges(self):
        """ 如果外星人位于屏幕边缘，返回True """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        