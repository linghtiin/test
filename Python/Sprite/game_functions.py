# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 19:23:26 2019

@author: z
"""
import sys
import pygame

from bullet import Bullet


def fire_bullet(ai_settings, screen, ship, bullets):
    """ 飞船开火"""
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
    
def check_keydown_even(even, ai_settings, screen, ship, bullets):
    """ 响应按键 """
    if even.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif even.key == pygame.K_LEFT:
        ship.moving_left = True
    elif even.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)


def check_keyup_even(even, ship):
    """ 响应松开 """
    if even.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif even.key == pygame.K_LEFT:
        ship.moving_left = False
    

def check_events(ai_settings, screen, ship, bullets):
    """ 游戏事件响应。 """
    for even in pygame.event.get():
        if even.type == pygame.QUIT:
            sys.exit()
        elif even.type == pygame.KEYDOWN:
            check_keydown_even(even, ai_settings, screen, ship, bullets)
        elif even.type == pygame.KEYUP:
            check_keyup_even(even, ship)

    
def update_screen(ai_settings, screen, ship, bullets):
    """ 屏幕更新。 """
    #重绘屏幕
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    
    #刷新屏幕
    pygame.display.flip()
    
def update_bullet(bullets):
    """ 全局子弹更新，控制 """
    bullets.update()
    
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    
    
    
    
    
    
    
    
    
    