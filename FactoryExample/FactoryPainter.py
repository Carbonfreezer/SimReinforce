# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 12:31:33 2025

@author: Luerig
"""

import pygame as pg
import Framework.PositionExtractor as Pos
import Framework.DiscreetBar as ProgPaint

class FactoryPainter:
    
    def __init__(self):
        self.__backGround = pg.image.load("Background.png")
        positionDict = {'Entrance' : [40,218],
                        'Exit':[1024-40,218],
                        'DepotA':[398.5, 218],
                        'DepotB': [618.5,218],
                        'Stat0' : [201,218],
                        'Stat1' : [513,73],
                        'Stat2' : [513,378],
                        'Stat3' : [823, 217],
                        'LeftP' : [201,522],
                        'RightP' : [823,522]
                            }
        self.__pointCollection = Pos.PositionExtractor(positionDict)
        
        
    
        
        pFunc = self.__pointCollection.GetPath
        self.__workerPathes={(0,1) : pFunc(['Stat0','Stat1']),
                             (0,2) : pFunc(['Stat0','Stat2']),
                             (0,3) : pFunc(['Stat0','LeftP','RightP','Stat3']),
                             (1,0) : pFunc(['Stat1','Stat0']),
                             (1,2) : pFunc(['Stat1','Stat2']),
                             (1,3) : pFunc(['Stat1','Stat3']),
                             (2,0) : pFunc(['Stat2','Stat0']),
                             (2,1) : pFunc(['Stat2','Stat1']),
                             (2,3) : pFunc(['Stat2','Stat3']),
                             (3,0) : pFunc(['Stat3','RightP', 'LeftP','Stat0']),
                             (3,1) : pFunc(['Stat3','Stat1']),
                             (3,2) : pFunc(['Stat3','Stat2'])
                           }
                             
                             
        self.__working = [pg.image.load("Working1.png"), pg.image.load("Working2.png")] 
        self.__travelling = [pg.image.load("Travelling1.png"), pg.image.load("Travelling2.png")]
        
        self.__depotPaint = ProgPaint.DiscreetBar(10, 3, 150, 75, 'Grey', 'Blue', 1)
        
                                                 
        
    
    @property
    def ImageSize(self):
        rect = self.__backGround.get_rect()
        return (rect.width, rect.height)
    
    def DrawStaticParts(self, surface):
        surface.blit(self.__backGround, (0,0))
        
        
    def DrawFinalOverlay(self, surface):
        # self.__pointCollection.DebugDraw(surface)
        pass
        
        
    def DrawElements(self, surface,  situations):
        # First we draw the depots,
        filling = situations['DA']['Info']
        self.__depotPaint.paint(surface,  self.__pointCollection.GetPoint('DepotA'),  filling)
        filling = situations['DB']['Info']
        self.__depotPaint.paint(surface,  self.__pointCollection.GetPoint('DepotB'),  filling)
        
        # Now come the actors
        for act in range(2):
            actorInfo = situations[f"A{act}"]["Info"]
            actorInterpol = situations[f"A{act}"]["Factor"]
            
            isWorking = actorInfo['State'] == 'Working'
            if isWorking:
                drawingPoint = self.__pointCollection.GetPoint(f"Stat{actorInfo['Station']}")
                drawingSprite = self.__working[act]
                Pos.PositionExtractor.PaintSprite(surface, drawingSprite, drawingPoint)
            else:
               travelPath = self.__workerPathes[(actorInfo['Station'], 
                                                 actorInfo['Destination'])]
               drawingPoint = Pos.PositionExtractor.GetInterpolatedPosition(travelPath, actorInterpol)
               drawingSprite = self.__travelling[act]
               Pos.PositionExtractor.PaintSprite(surface, drawingSprite, drawingPoint)
               
        
      
    