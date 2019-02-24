# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 11:54:55 2019

@author: z
"""
import pygame
from pygame.sprite import Group

import game_functions as gf
from settings import Settings
from ship import Ship


def run_game():
    """" 运行游戏。 """
    pygame.init()
    ai_setting = Settings()
    pygame.display.set_caption("Alien Invasion")
    
    screen =pygame.display.set_mode(
        (ai_setting.screen_width,ai_setting.screen_height))
    
    #创建游戏物体
    ship = Ship(ai_setting, screen)
    bullets = Group()
    
    #临时变量
    
    #游戏主循环
    while True:
        
        gf.check_events(ai_setting, screen, ship, bullets)
        ship.update()
        gf.update_bullet(bullets)
        gf.update_screen(ai_setting, screen, ship, bullets)

    
    
    
    
    
    
    
#运行测试    
run_game()
