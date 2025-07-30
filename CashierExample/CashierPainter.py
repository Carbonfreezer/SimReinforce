# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 09:05:27 2025

@author: Luerig
"""

import pygame as pg
import Framework.Graphics.PositionManager as Pos
import Framework.Graphics.DiscreetBar as Discreet
import Framework.Graphics.ContinuousBar as Continuos

class CashierPainter:
    
    def __init__(self):
        '''
        The example cashier painter initializes all, that is required to paint a given situation of the cashier.

        Returns
        -------
        None.

        '''
      
        positionDict = {
                        # Entrance positions
                        'EntranceA' : [0,290],
                        'EntranceB' : [40, 290],
                        'Dispatcher' : [100, 290],
                        
                         # Que positions.
                        'Que0S' : [200, 145],
                        'Que1S' : [200, 290],
                        'Que2S' : [200, 435],
                        
                        'Que0M' : [450, 145],
                        'Que1M' : [450, 290],
                        'Que2M' : [450, 435],
                        
                        'Que0E' : [700, 145],
                        'Que1E' : [700, 290],
                        'Que2E' : [700, 435],
                        
                        # Exit positions
                        'Cash0E' : [900, 145],
                        'Cash1E' : [900, 290],
                        'Cash2E' : [900, 435],
                        
                        'ExitA' : [984, 290],
                        'ExitB' : [1023, 290],
                        
                        # Additional points relevant for the cashiers.
                        'Place0' : [800, 95],
                        'Place1' : [800, 245],
                        'Place2' : [800, 390],
                        'Side0' : [900, 95],
                        'Side1' : [900, 245],
                        'Side2' : [900, 390],
                        
                       # The coordinates for the bottom.
                       'Time' : [415, 675],
                       'ItemText' : [900, 700]
                }
        
        
        self.__pointCollection = Pos.PositionManager(positionDict)
        
        
    
        
        pFunc = self.__pointCollection.GetPath
        
        self.__entrancePathes = [pFunc(['EntranceA', 'EntranceB', 'Dispatcher', 'Que0S']),
                                pFunc(['EntranceA', 'EntranceB', 'Dispatcher', 'Que1S']),
                                pFunc(['EntranceA', 'EntranceB', 'Dispatcher', 'Que2S'])]
        self.__custCash = [pFunc(['Que0E', 'Cash0E']),
                                pFunc(['Que1E', 'Cash1E']),
                                pFunc(['Que2E', 'Cash2E'])
                                ]
        
        self.__exitPathes = [pFunc(['Cash0E', 'ExitA','ExitB']),
                             pFunc(['Cash1E', 'ExitA','ExitB']),
                             pFunc(['Cash2E', 'ExitA','ExitB'])
                             ]
        
        self.__cashierPathes = {}
        for source in range(3):
            for dest in range(3):
                self.__cashierPathes[(source, dest)] = pFunc([f"Place{source}",
                                                              f"Side{source}",
                                                              f"Side{dest}",
                                                              f"Place{dest}"
                                                              ])
        
        
        
        
            
                             
        self.__backGround = pg.image.load("Media/Background.png")                         
        self.__foreGround = pg.image.load("Media/Foreground.png")   
        
        self.__custImage = pg.image.load("Media/Customer.png")
        self.__arrow = pg.image.load("Media/Arrow.png")
        
        self.__cross = pg.image.load("Media/Cross.png")
        
        
        self.__slowImages = {'Working' : pg.image.load("Media/SlowWorking.png"),
                             'Walking' : pg.image.load("Media/SlowTravelling.png"),
                             'Stalled' : pg.image.load("Media/SlowStalled.png")}
        self.__fastImages = {'Working' : pg.image.load("Media/FastWorking.png"),
                             'Walking' : pg.image.load("Media/FastTravelling.png"),
                             'Stalled' : pg.image.load("Media/FastStalled.png")}
        
        
        
        self.__queBar = Discreet.DiscreetBar(10, 3, 500, 40,'Grey', 'Blue', 3)
        ''' The bar for the ques '''
        self.__timePaint = Continuos.ContinuousBar(10, 730, 150, 'Grey', 'Blue', 3)
        ''' The time bar '''
        
        
        
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
        
        pointGet = self.__pointCollection.GetPoint
        # First background
        surface.blit(self.__backGround, (0,0))
        
       
        # Then we draw the ques.
        for que in range(3):
            filling = situations[f"Que{que}"]['Info']
            self.__queBar.paint(surface, pointGet(f"Que{que}M"), filling)
            
        # If we are busted we draw the cross
        if 'QueBusted' in situations:
            bustedQue = situations['QueBusted']['Info']
            Pos.PositionManager.PaintSprite(surface, self.__cross, pointGet(f"Que{bustedQue}M"))
            
    
        
        # Now we draw all leaving customers, that is a bit tricky, as we have to cycle over them.
        leavingCustomers = (x for x in situations.keys() if x.startswith("LeavingCust"))
        for cust in leavingCustomers:
            path = situations[cust]
            drawingPoint = Pos.PositionManager.GetInterpolatedPosition(self.__exitPathes[path['Info']], 
                                                                       path['Progress'])
            Pos.PositionManager.PaintSprite(surface, self.__custImage, drawingPoint)
            
        # Now we draw the dispatcher.
        if 'LastDispatch' in situations:
            orientation = situations['LastDispatch']['Info']
            sourcePoint = pointGet("Dispatcher")
            destinationPoint = pointGet(f"Que{orientation}S")
            Pos.PositionManager.PaintSpritePointing(surface, self.__arrow, sourcePoint, destinationPoint)
            # Get the customer painted.
            drawingPoint = Pos.PositionManager.GetInterpolatedPosition(self.__entrancePathes[orientation], 
                                                                       situations['LastDispatch']['Progress'])
            Pos.PositionManager.PaintSprite(surface, self.__custImage, drawingPoint)
        
        # Now the cashiers.
        for index, element in enumerate([situations["CashSlow"], situations["CashFast"]]):
              imageArray = self.__slowImages if index == 0 else self.__fastImages
              info = element['Info']
              que = info['Station']
              match info['State']:
                  case 'Stalled':
                      Pos.PositionManager.PaintSprite(surface, imageArray['Stalled'], 
                                                      pointGet(f"Place{que}"))
                  case 'Walking':
                      animationPath = self.__cashierPathes[(que, info['Destination'])]
                      pos =  Pos.PositionManager.GetInterpolatedPosition(animationPath, 
                                                                         element['Progress'])
                      Pos.PositionManager.PaintSprite(surface, imageArray['Walking'], pos)
                  case 'Working':
                      Pos.PositionManager.PaintSprite(surface, imageArray['Working'], 
                                                      pointGet(f"Place{que}"))
                      custPos = Pos.PositionManager.GetInterpolatedPosition(self.__custCash[que], 
                                                                            element['Progress'])
                      Pos.PositionManager.PaintSprite(surface, self.__custImage, custPos)
               
        # The bottom bar
        numCustomers = situations['Custs']['Info']
        img = self.__font.render(f"{numCustomers}", True, pg.Color(255,255,255))
        Pos.PositionManager.PaintSprite(surface, img, pointGet("ItemText"))
        time = situations['Time']['Progress']
        self.__timePaint.paint(surface,  pointGet("Time"),  1.0 - time)
        
        # Final overlay
        surface.blit(self.__foreGround, (0,0))
        # self.__pointCollection.DebugDraw(surface)
       
               
        
      
    