# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 11:19:38 2025

@author: Luerig
"""

import pygame as pg
import numpy as np

class PositionManager:
    def __init__(self, pointDictionary):
        
        
        self.__font = pg.font.SysFont(None, 32)
        self.__pointDictionary = {}
        for key,value in pointDictionary.items():
            self.__pointDictionary[key] = np.array(value)
        
        
        
    def DebugDraw(self, targetSurface):
        for idx, point in enumerate(self.__pointDictionary):
            img = self.__font.render(f"{idx}", True, pg.Color(255,255,255))
            self.PaintSprite(targetSurface, img, point)
            
    
    @property
    def NumOfPoints(self):
        return np.shape(self.__pointDictionary)[0]
    
    def GetPoint(self, index):
        return self.__pointDictionary[index]
    
    
    @staticmethod
    def PaintSprite(destination, source, point):
        rect = source.get_rect()
        targetPoint = point - [rect.width * 0.5, rect.height * 0.5]
        destination.blit(source, targetPoint)
    
    def GetPath(self, listOfPoints):
        result = []
        totalLength = 0.0
        for i in range(len(listOfPoints)-1):
            start = self.__pointDictionary[listOfPoints[i]]
            end = self.__pointDictionary[listOfPoints[i + 1]]
            length = np.linalg.norm(end - start)
            totalLength += length
            entry = {'Start' : start, 'End' : end, 'Length' : length}
            result.append(entry)
        return (totalLength, result)

    @staticmethod
    def GetInterpolatedPosition(path, interPol):
        remaining, segments = path
        remaining *= interPol
        scanning = 0
        while remaining - segments[scanning]['Length'] > 0.0:
            remaining = remaining - segments[scanning]['Length']
            scanning += 1
        
        localF = remaining /  segments[scanning]['Length']
        result = segments[scanning]['Start'] + \
            (segments[scanning]['End'] - segments[scanning]['Start']) * localF
            
        return result
            
        
        
        