# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 09:44:22 2025

@author: chris
"""


import pygame as pg

class Bar():
    def __init__(self,  insetWidth, width, height, bgColor,  fgColor, orientation):
        '''
        Super class for continuous and discreet progress bar.

        Parameters
        ----------
        insetWidth :  
            distance between bar and border and in discreet mode also for the segments.
        width :  
            width of the bar in pixels.
        height :  
            height of the bar in pixels.
        bgColor :  
            background color of the bar.
        fgColor :  
            foreground color of the bar.
        orientation :  
            orientation 0 : downwards, 1 : right, 2: updwards, 3 : left

        Returns
        -------
        None.

        '''
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