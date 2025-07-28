# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 15:50:32 2025

@author: Luerig
"""

import pygame as pg

import Framework.Graphics.Bar as Bar


class DiscreetBar(Bar.Bar):
    def __init__(self, maxEntries,  insetWidth, width, height, bgColor,  fgColor, orientation):
        '''
        Creates the dsicreet segmented bar.

        Parameters
        ----------
        maxEntries :  
            The maximum integer value we can represent.
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
        super().__init__( insetWidth, width, height, bgColor,  fgColor, orientation)
        self.__maxEntries = maxEntries


        
         
        
        
    def paint(self, targetSurface, position, entries):
        '''
        Paints the bar at a given position and value.

        Parameters
        ----------
        targetSurface :  
            Pygame surface where to draw the bar to.
        position :  
            Center position of the bar.
        entries :  
            Amounts of segments to display.

        Returns
        -------
        None.

        '''
        
        stepHeight = self._sourceHeight / self.__maxEntries
        targetWidth = self._sourceWidth - 2 * self._insetWidth
        targetHeight = stepHeight - 2 * self._insetWidth
        xPos = self._insetWidth
        yPos = self._insetWidth
        
        self._drawSurface.fill( self._bgColor)
        for _ in range(entries):
            pg.draw.rect(self._drawSurface,  self._fgColor, pg.Rect(xPos, yPos, targetWidth, targetHeight))
            yPos += stepHeight
                
        finalImage = pg.transform.rotate(self._drawSurface, self._turningAngle)
        targetSurface.blit(finalImage,  (position[0] - self._destWidth * 0.5, position[1] - self._destHeight * 0.5))  