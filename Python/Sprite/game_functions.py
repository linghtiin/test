# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 19:23:26 2019

@author: z
"""
import sys
import pygame

from bullet import Bullet
from aline import Aline
from time import sleep

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
    elif even.key == pygame.K_q:
        sys.exit()


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

    
def update_screen(ai_settings, screen, ship, alines, bullets):
    """ 屏幕更新。 """
    #重绘屏幕
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    alines.draw(screen)
#    for aline in alines.sprites():
#        aline.blitme()
    
    #刷新屏幕
    pygame.display.flip()
    
def creat_fleet(ai_settings, screen, alines):
    """ 外星敌人群生成 """
    aline = Aline(ai_settings, screen)
    aline_width = aline.rect.width
    aline_height = aline.rect.height
    
    number_alines_x = get_number_aline_x(ai_settings, aline_width)
    number_row = get_number_aline_y(ai_settings, aline_height)
    
    for row_number in range(number_row):
        for aline_number in range(number_alines_x):
            creat_aline(ai_settings, screen, alines, aline_number, row_number)
        

def get_number_aline_x(ai_settings, aline_width):
    """ 获取外星人单行生成数 """
    available_space_x = ai_settings.screen_width - 2 * aline_width
    number_alines_x = int(available_space_x / (2 * aline_width))
    return number_alines_x
    
def get_number_aline_y(ai_settings, aline_height):
    """ 获取外星人单列生成数 """
    available_space_y = int(ai_settings.screen_height * 0.6)
    number_row = int(available_space_y / (2 * aline_height))
    return number_row
    
def creat_aline(ai_settings, screen, alines, aline_number, row_number):
    """ 创建一个外星人并放入当前行 """
    aline = Aline(ai_settings, screen)
    aline_width = aline.rect.width
    aline.x = aline_width + 2 * aline_width * aline_number
    aline.rect.x = aline.x
    aline.rect.y = aline.rect.height + 2 * aline.rect.height * row_number
    alines.add(aline)
    
    
def check_fleet_edges(ai_settings, alines):
    """ 有外星人到达边缘时，行为 """
    for aline in alines.sprites():
        if aline.check_edges():
            change_fleet_direction(ai_settings, alines)
            break
        
def change_fleet_direction(ai_settings, alines):
    """ 整群外星人下移，并改变方向 """
    for aline in alines.sprites():
        aline.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
   
def ship_hit(ai_settings, stats, screen, ship, alines, bullets):
    """ 响应被外星人撞到的飞船 """
    if stats.ship_left > 0:
        stats.ship_left -= 1
        
        alines.empty()
        bullets.empty()
        creat_fleet(ai_settings, screen, alines)
        ship.center_ship()
        
        sleep(0.5)
    else:
        stats.game_active = False
        print("Game over !!!")

     
def update_alines(ai_settings, stats, screen, ship, alines, bullets):
    """ 更新外星人 """
    check_fleet_edges(ai_settings, alines)
    alines.update()
    
    #检测外星人与飞船的碰撞
    if pygame.sprite.spritecollideany(ship, alines):
        print("Ship hit !!!")
        ship_hit(ai_settings, stats, screen, ship, alines, bullets)
    check_alien_buttom(ai_settings, stats, screen, ship, alines, bullets)
    
def update_bullet(ai_settings, screen, alines, bullets):
    """ 全局子弹更新，控制 """
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, alines, bullets)
   
def check_bullet_alien_collisions(ai_settings, screen, alines, bullets):
    """ 检测外星人与子弹的碰撞 """
    #删除外星人与子弹
    collisions = pygame.sprite.groupcollide(bullets, alines, True, True)
    
    if len(alines) == 0:
        bullets.empty()
        creat_fleet(ai_settings, screen, alines)
        
def check_alien_buttom(ai_settings, stats, screen, ship, alines, bullets):
    """ 检查外星人是否到达低端 """
    screen_rect = screen.get_rect()
    for aline in alines.sprites():
        if aline.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, alines, bullets)
            break
        
    
    
    
    
    
    
    
    
    

    
    
    
    
    
    
    
    
    