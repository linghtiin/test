# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 15:42:16 2019

@author: z
"""

class GameStats():
    """ 用于统计游戏信息的类。 """
    def __init__(self, ai_settings):
        """ 初始化统计信息 """
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = True
    
    def reset_stats(self):
        """ 初始化运行信息。 """
        self.ship_left = self.ai_settings.ship_limit
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    