# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 16:02:49 2019

@author: 10127
"""

import pygame.font

class Scoreboard():
    """  """
    def __init__(self, ai_settings, screen, stats):
        """  """
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 30)
        
        self.prep_score()
        self.prep_high_score()
        
    def prep_score(self):
        """ 文字预渲染 """
        rounded_score = int(round(self.stats.sore, -1))
        score_str = "{:,}pt".format(rounded_score)
        
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.ai_settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        
    def prep_high_score(self):
        """  """
        pass
    
    def show_score(self):
        """  """
        self.screen.blit(self.score_image, self.score_rect)
        
        
        
        
        
        
        
        
        