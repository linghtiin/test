# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 01:59:45 2019

@author: z
"""
import os
import numpy as np
import pandas as pd

workpath = os.getcwd()
whiskies = pd.read_csv(workpath + '\\' + 'whiskies.txt')
whiskies['Region'] = pd.read_csv(workpath + '\\' + 'regions.txt')

#相关性矩阵
corr_whiskies = pd.DataFrame.corr(whiskies)

