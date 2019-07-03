# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 11:15:36 2019

@author: 10127
"""

import re

s = 'nisa sina lisa monika modi nisa'

b1 = re.match(r'nisa', s)
q = b1.group()

a = re.compile(r'nisa')
b2 = a.match(s)
q2 = b2.group()

d1 = re.findall(r'nisa', s)
d2 = re.search(r'nisa', s)
q3 = d2.group()
