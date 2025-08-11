# -*- coding: utf-8 -*-
"""
Created on Sat Aug  9 14:34:26 2025

@author: chris
"""

class EmergencyCall:
    
    def __init__(self, category, startTime, region):
        self.__category = category
        self.__startTime = startTime
        self.__region = region
    
        
    
        
    @property
    def Category(self):
        return self.__category
    
    @property
    def StartTime(self):
        return self.__startTime
    
    
    @property
    def Region(self):
        return self.__region
    