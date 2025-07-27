# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 09:44:22 2025

@author: chris
"""


import pygame as pg

class Bar():
    def __init__(self,  insetWidth, width, height, bgColor,  fgColor, orientation):
        self._insetWidth = insetWidth
        self._bgColor = bgColor
        self._fgColor = fgColor
        self._destWidth , self._destHeight = width , height
      
        
        match(orientation):
            case 0:
                self._turningAngle = 0
                self._sourceWidth , self._sourceHeight = width, height
            case 1:
                self._turningAngle = 90
                self._sourceWidth , self._sourceHeight = height, width 
            case 2:
                self._turningAngle = 180
                self._sourceWidth , self._sourceHeight = width, height
            case 3:
                self._turningAngle = 270
                self._sourceWidth , self._sourceHeight = height, width

        self._drawSurface = pg.Surface((self._sourceWidth, self._sourceHeight))