# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 19:05:12 2019

@author: z
"""
import os
import pygame


class Ship():
    """ 飞船类 """
    
    def __init__(self, ai_settings, screen):
        """ 初始化飞船 """
        self.screen = screen
        self.ai_settings = ai_settings
        
        #加载飞船图像与碰撞体'.//image//ship.bmp'
        self.image = pygame.image.load(r".\image\ship.png")
        #self.image = pygame.image.load(os.path.join('image', 'ship.bmp'))
        self.rect = self.image.get_rect()
#        self.rect = pygame.Rect(0, 0, 26, 24)     #test
        self.screen_rect = screen.get_rect()
        
        #初始位置
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        #浮点位置
        self.center = float(self.rect.centerx)
        
        #移动标志
        self.moving_right = False
        self.moving_left = False
        
        
    def update(self):
        """ 飞船状态更新 """
        #移动
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
            
        self.rect.centerx = self.center
            
        
    def blitme(self):
        """ 在指定位置绘制飞船"""
#        pygame.draw.rect(self.screen, (0, 255, 0), self.rect)  #test
        self.screen.blit(self.image, self.rect)
        
    def center_ship(self):
        """ 使飞船在屏幕上居中 """
        self.center = self.screen_rect.centerx
        
        
        
        
        
        
        
        
        
        