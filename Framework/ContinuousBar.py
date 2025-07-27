# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 15:50:32 2025

@author: Luerig
"""

import pygame as pg

import Framework.Bar as Bar


class ContinuousBar(Bar.Bar):
    def __init__(self,  insetWidth, width, height, bgColor,  fgColor, orientation):
        super().__init__( insetWidth, width, height, bgColor,  fgColor, orientation)
       
      
        
        
        
    def paint(self, targetSurface, position, value):
        
        targetWidth = self._sourceWidth - 2 * self._insetWidth
        targetHeight = self._sourceHeight * value - 2 * self._insetWidth
        xPos = self._insetWidth
        yPos = self._insetWidth
        self._drawSurface.fill( self._bgColor)
        pg.draw.rect(self._drawSurface,  self._fgColor, pg.Rect(xPos, yPos, targetWidth, targetHeight))
            
            
        finalImage = pg.transform.rotate(self._drawSurface, self._turningAngle)
        targetSurface.blit(finalImage,  (position[0] - self._destWidth * 0.5, position[1] - self._destHeight * 0.5))    
        