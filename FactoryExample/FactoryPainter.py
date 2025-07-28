# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 12:31:33 2025

@author: Luerig
"""

import pygame as pg
import Framework.PositionManager as Pos
import Framework.DiscreetBar as Discreet
import Framework.ContinuousBar as Continuos

class FactoryPainter:
    
    def __init__(self):
        '''
        The example factor painter initializes all, that is required to paint a given situation of the factory.

        Returns
        -------
        None.

        '''
      
        positionDict = {'Entrance' : [40,218],
                        'Exit':[1024-40,218],
                        'DepotA':[398.5, 218],
                        'DepotB': [618.5,218],
                        'Stat0' : [201,218],
                        'Stat1' : [513,73],
                        'Stat2' : [513,378],
                        'Stat3' : [823, 217],
                        'LeftP' : [201,522],
                        'RightP' : [823,522],
                        'ObjT' : [935, 725],
                        'Bar' : [412,692]
                            }
        self.__pointCollection = Pos.PositionManager(positionDict)
        
        
    
        
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
        
        self.__objectPathes = [pFunc(['Entrance', 'Stat0', 'DepotA']),
                               pFunc(['DepotA', 'Stat1', 'DepotB']),
                               pFunc(['DepotA', 'Stat2', 'DepotB']),
                               pFunc(['DepotB','Stat3', 'Exit'])]
            
                             
        self.__backGround = pg.image.load("Media/Background.png")                         
        self.__foreGround = pg.image.load("Media/Foreground.png")   
        self.__working = [pg.image.load("Media/Working1.png"), pg.image.load("Media/Working2.png")] 
        self.__travelling = [pg.image.load("Media/Travelling1.png"), pg.image.load("Media/Travelling2.png")]
        self.__stalled = [pg.image.load("Media/Stalled1.png"), pg.image.load("Media/Stalled2.png")]
        
        self.__depotPaint = Discreet.DiscreetBar(10, 3, 150, 75, 'Grey', 'Blue', 1)
        self.__objectImage = pg.image.load("Media/Product.png")
        self.__timePaint = Continuos.ContinuousBar(10, 799, 118, 'Grey', 'Blue', 3)
        
        self.__font = pg.font.SysFont(None, 48)
        
        
                                                 
        
    
    @property
    def ImageSize(self):
        '''
        Returns the size of the background image and therefore the video

        Returns
        -------
            Pair of width and height of the desired video.

        '''
        rect = self.__backGround.get_rect()
        return (rect.width, rect.height)
        
        
    def DrawScene(self, surface,  situations):
        '''
        Paints the complete situation onto a surface.

        Parameters
        ----------
        surface :  
            The surface where to paint the situation to.
        situations :  
            The dictionary with the current situation. 
            This dictionary is associating the name of an actor with another dictionary.
            This dictionary has the entries 'Progress' which is s float between [0,1] 
            and can be used to map the situation to a continuous change, and an entry 'Info' which is arbitrary data
            from the logging system.

        Returns
        -------
        None.

        '''
        # First background
        surface.blit(self.__backGround, (0,0))
        # First we draw the depots,
        filling = situations['DA']['Info']
        self.__depotPaint.paint(surface,  self.__pointCollection.GetPoint('DepotA'),  filling)
        filling = situations['DB']['Info']
        self.__depotPaint.paint(surface,  self.__pointCollection.GetPoint('DepotB'),  filling)
        
        # Now come the actors
        for act in range(2):
            actorInfo = situations[f"A{act}"]["Info"]
            actorInterpol = situations[f"A{act}"]["Progress"]
            
            if actorInfo['State'] == 'Working':
                drawingPoint = self.__pointCollection.GetPoint(f"Stat{actorInfo['Station']}")
                drawingSprite = self.__working[act]
                Pos.PositionManager.PaintSprite(surface, drawingSprite, drawingPoint)
                # Now we draw the parcel.
                drawingPoint = Pos.PositionManager.GetInterpolatedPosition(self.__objectPathes[actorInfo['Station']], actorInterpol)
                Pos.PositionManager.PaintSprite(surface, self.__objectImage, drawingPoint)
            elif actorInfo['State'] == 'Stalled':
                drawingPoint = self.__pointCollection.GetPoint(f"Stat{actorInfo['Station']}")
                drawingSprite = self.__stalled[act]
                Pos.PositionManager.PaintSprite(surface, drawingSprite, drawingPoint)
            else:
               travelPath = self.__workerPathes[(actorInfo['Station'], 
                                                 actorInfo['Destination'])]
               drawingPoint = Pos.PositionManager.GetInterpolatedPosition(travelPath, actorInterpol)
               drawingSprite = self.__travelling[act]
               Pos.PositionManager.PaintSprite(surface, drawingSprite, drawingPoint)
               
               
        # The bottom bar
        numItems = situations['Objs']['Info']
        img = self.__font.render(f"{numItems}", True, pg.Color(255,255,255))
        Pos.PositionManager.PaintSprite(surface, img, self.__pointCollection.GetPoint("ObjT"))
        time = situations['Time']['Progress']
        self.__timePaint.paint(surface,  self.__pointCollection.GetPoint('Bar'),  1.0 - time)
        
        # Final overlay
        surface.blit(self.__foreGround, (0,0))
        # self.__pointCollection.DebugDraw(surface)
       
               
        
      
    