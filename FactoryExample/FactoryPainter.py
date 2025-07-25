# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 12:31:33 2025

@author: Luerig
"""

import pygame as pg
import Framework.PositionExtractor as Pos
import Framework.ProgressBarPainter as ProgPaint

class FactoryPainter:
    
    def __init__(self):
        self.__backGround = pg.image.load("Background.png")
        self.__pointCollection = Pos.PositionExtractor("Positions.png")
    
        
        self.__workerPositionCoordinates = [1, 0, 3, 2]
        self.__workerPathes={(0,1) : self.__pointCollection.GetPath([1,0]),
                             (0,2) : self.__pointCollection.GetPath([1,3]),
                             (0,3) : self.__pointCollection.GetPath([1,4,5,2]),
                             (1,0) : self.__pointCollection.GetPath([0,1]),
                             (1,2) : self.__pointCollection.GetPath([0,3]),
                             (1,3) : self.__pointCollection.GetPath([0,2]),
                             (2,0) : self.__pointCollection.GetPath([3,1]),
                             (2,1) : self.__pointCollection.GetPath([3,0]),
                             (2,3) : self.__pointCollection.GetPath([3,2]),
                             (3,0) : self.__pointCollection.GetPath([2,5,4,1]),
                             (3,1) : self.__pointCollection.GetPath([2,0]),
                             (3,2) : self.__pointCollection.GetPath([3,1])}
                             
                             
        self.__working = [pg.image.load("Working1.png"), pg.image.load("Working2.png")] 
        self.__travelling = [pg.image.load("Travelling1.png"), pg.image.load("Travelling2.png")]
        
        self.__depotPaint = ProgPaint.ProgressBarPainter(10, 3, 80, 160, 'Blue')
        
                                                 
        
    
    @property
    def ImageSize(self):
        rect = self.__backGround.get_rect()
        return (rect.width, rect.height)
    
    def DrawStaticParts(self, surface):
        surface.blit(self.__backGround, (0,0))
        
        
    def DrawFinalOverlay(self, surface):
        # self.__pointCollection.DebugDraw(surface)
        pass
        
        
    def DrawElement(self, surface, actor, interpolationTime, interpolationInformation):
        '''
        Draws a time dependend element into the surface

        Parameters
        ----------
        surface : TYPE
            Destination surface to render to.
        actor : TYPE
            The actor we want to render.
        interpolationTime : TYPE
            The transition state (0..1) the actor is in.
        interpolationInformation : TYPE
            Specific information added to generate the image.

        Returns
        -------
        None.

        '''
        
        if actor in ['A0', 'A1']:
            index = 0 if actor=='A0' else 1
            isWorking = interpolationInformation['State'] == 'Working'
            if isWorking:
                drawingPoint = self.__pointCollection.GetPoint(
                    self.__workerPositionCoordinates[interpolationInformation['Station']])
                drawingSprite = self.__working[index]
                Pos.PositionExtractor.PaintSprite(surface, drawingSprite, drawingPoint)
            else:
               travelPath = self.__workerPathes[(interpolationInformation['Station'], 
                                                 interpolationInformation['Destination'])]
               drawingPoint = Pos.PositionExtractor.GetInterpolatedPosition(travelPath, interpolationTime)
               drawingSprite = self.__travelling[index]
               Pos.PositionExtractor.PaintSprite(surface, drawingSprite, drawingPoint)
               
        elif actor == 'DA':
           self.__depotPaint.paint(surface, (422, 300), 180, interpolationInformation)
        else:
           self.__depotPaint.paint(surface, (601, 300), 180, interpolationInformation) 
    