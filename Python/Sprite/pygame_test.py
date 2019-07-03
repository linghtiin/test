# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 11:54:55 2019

@author: z
"""
import pygame
from pygame.sprite import Group

import game_functions as gf
from settings import Settings
from game_stats import GameStats
from ship import Ship
from button import Button
from scoreboard import Scoreboard

def run_game():
    """" 运行游戏。 """
    pygame.init()
    ai_setting = Settings()
    pygame.display.set_caption("Alien Invasion")
    
    screen =pygame.display.set_mode(
        (ai_setting.screen_width,ai_setting.screen_height))
    
    #创建游戏物体
    play_button = Button(ai_setting, screen, 'Play')
    stats = GameStats(ai_setting)
    sb = Scoreboard(ai_setting, screen, stats)
    
    ship = Ship(ai_setting, screen)
    alines = Group()
    bullets = Group()
    
    #临时变量
    gf.creat_fleet(ai_setting, screen, alines)
    
    #游戏主循环
    while True:
        
        gf.check_events(ai_setting, screen, alines, bullets, ship, stats,
                        play_button)
        
        if stats.game_active:
            ship.update()
            gf.update_bullet(ai_setting, screen, alines, bullets, stats, sb)
            gf.update_alines(ai_setting, stats, screen, ship, alines, bullets)
        
        gf.update_screen(ai_setting, screen, stats, ship, alines, bullets,
                         play_button, sb)

    
    
    
    
def test_game():
    """ 测试函数 """
    
    
#运行测试    
run_game()
