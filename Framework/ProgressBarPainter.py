# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 15:50:32 2025

@author: Luerig
"""

import pygame as pg


class ProgressBarPainter():
    def __init__(self, maxEntries, insetWidth, width, height, color):
        self.__maxEntries = maxEntries
        self.__insetWidth = insetWidth
        self.__color = color
        self.__drawSurface = pg.Surface((width, height))
        
        
    def paint(self, targetSurface, position, turningAngle, entries):
        width =  self.__drawSurface.get_rect().width
        height =  self.__drawSurface.get_rect().height
        
        targetWidth = width - 2 * self.__insetWidth
        targetHeight = height / self.__maxEntries - 2 * self.__insetWidth
        stepHeight = height / self.__maxEntries
        xPos = self.__insetWidth
        yPos = self.__insetWidth
        self.__drawSurface.fill("Grey")
        for _ in range(entries):
            pg.draw.rect(self.__drawSurface, self.__color, pg.Rect(xPos, yPos, targetWidth, targetHeight))
            yPos += stepHeight
            
            
        finalImage = pg.transform.rotate(self.__drawSurface, turningAngle)    
        targetSurface.blit(finalImage,  (position[0] - width * 0.5, position[1] - height * 0.5))    
        