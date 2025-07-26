# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 15:50:32 2025

@author: Luerig
"""

import pygame as pg




class ContinuousBar():
    def __init__(self,  insetWidth, width, height, bgColor,  fgColor, orientation):
        self.__insetWidth = insetWidth
        self.__bgColor = bgColor
        self.__fgColor = fgColor
        if orientation == 0: # Down
            self.__turningAngle = 0
        elif orientation == 1: # Right
            self.__turningAngle = 90
            width, height = height, width
        elif orientation == 2: # Up
            self.__turningAngle = 180
        else: # left
            self.__turningAngle = 270
            width, height = height, width
        self.__drawSurface = pg.Surface((width, height))
        
        
    def paint(self, targetSurface, position, value):
        width =  self.__drawSurface.get_rect().width
        height =  self.__drawSurface.get_rect().height
        
        targetWidth = width - 2 * self.__insetWidth
        targetHeight = height * value - 2 * self.__insetWidth
        xPos = self.__insetWidth
        yPos = self.__insetWidth
        self.__drawSurface.fill( self.__bgColor)
        pg.draw.rect(self.__drawSurface,  self.__fgColor, pg.Rect(xPos, yPos, targetWidth, targetHeight))
            
            
        finalImage = pg.transform.rotate(self.__drawSurface, self.__turningAngle)
        width =  finalImage.get_rect().width
        height =  finalImage.get_rect().height
        targetSurface.blit(finalImage,  (position[0] - width * 0.5, position[1] - height * 0.5))    
        