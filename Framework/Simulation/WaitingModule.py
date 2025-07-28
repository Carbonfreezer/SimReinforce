# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 14:20:46 2025

@author: Luerig
"""


class WaitingModule:
    def __init__(self, simpyEnv, random):
        self.__simpyEnv = simpyEnv
        self.__random = random
        
        
        
    def WaitExponential(self, mean):
        yield self.__simpyEnv.timeout(self.__random.exponential(scale=mean))
        
    def WaitGamma(self,inVal):
        
        mean, std = inVal
        scale = (std ** 2) / mean
        shape = mean / scale
        
        yield self.__simpyEnv.timeout(self.__random.gamma(shape, scale))
        
        