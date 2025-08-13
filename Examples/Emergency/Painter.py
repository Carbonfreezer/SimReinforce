# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 08:08:18 2025

@author: chris
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 12:31:33 2025

@author: Luerig
"""

import pygame as pg
import Framework.Graphics.PositionManager as Pos
import Framework.Graphics.ContinuousBar as Continuos
import Framework.Graphics.SpriteHelper as Sprite

class Painter:
    
    def __init__(self):
        '''
        The example factor painter initializes all, that is required to paint a given situation of the factory.

        Returns
        -------
        None.

        '''
        
        totalHeight = 1080
        stride = 1800 / 8
        
        
        positionDict = {}
        
        
        # The positions for the three incoming calls.
        incomingOffset = 200
        for i in range(3):
            positionDict[('InCall', i)] = [stride * 0.5, totalHeight / 2 + (i - 1) * incomingOffset]
            
        # The positions for the 8 call takers.
        yStride = totalHeight / 8
        for i in range(8):
            positionDict[('Taker', i)] = [stride * 1.5, yStride * (i + 0.5)]
            
        # The position for the 2 * 3 dispatched calls, running calls and the dispatcher.
        for dispatcher in range(2):
            for prio in range(3):
                positionDict[('Dispatched', dispatcher, prio)] = \
                    [stride * 2.5, dispatcher * (totalHeight / 2) + yStride * (prio + 0.5) ]
                positionDict[('Running', dispatcher, prio)] = \
                     [stride * 6.5, dispatcher * (totalHeight / 2) + yStride * (prio + 0.5) ] 
            positionDict[('Dispatcher', dispatcher)] = [stride * 4.5, totalHeight / 2 * (dispatcher + 0.5)]    
            for ressource in range(2):
                xpos = stride * ( 3.5 if ressource == 0 else 5.5)
                ypos = totalHeight / 2 - 150 if dispatcher == 0 else totalHeight / 2 + 150
                positionDict[('Ressource', dispatcher,ressource)] = [xpos, ypos]
                
        positionDict['Target'] = [stride * 7.5, totalHeight / 2] 
        positionDict['Time'] = [stride * 7.5, totalHeight / 2 + 100]
        positionDict['Bar'] = [1860, totalHeight / 2] 
                           
      
        # The ressources are hard coded (Dispatcher, ressourceType)
                     
      
        self.__pointCollection = Pos.PositionManager(positionDict)
        
        
        pFunc = self.__pointCollection.GetPath
        
        # The calltaker pathes consisting of prio, callTaker and dispatcher
        self.__callTakerPathes = { (prio, callTaker, dispatcher) : 
                                  pFunc([('InCall', prio), ('Taker', callTaker), ('Dispatched', dispatcher, prio)]) 
                                  for prio in range(3) for callTaker in range(8) for dispatcher in range(2)}
        
        self.__executionPathes = {(dispatcher, prio) : 
                                  pFunc([('Dispatched', dispatcher, prio), ('Dispatcher', dispatcher), ('Running', dispatcher, prio)])
                                  for dispatcher in range(2) for prio in range(3)
                                  }
            
        self.__resorceAssignmentPathes = {(dispatcher, prio, ressource):
                                  pFunc([('Ressource', dispatcher, ressource), ('Dispatcher', dispatcher), ('Running', dispatcher, prio)])
                                  for dispatcher in range(2) for prio in range(3) for ressource in range(2)}
            
        self.__directReturnPathes =  {(dispatcher, prio, ressource):
                                  pFunc([('Running', dispatcher, prio),('Ressource', dispatcher, ressource)])
                                  for dispatcher in range(2) for prio in range(3) for ressource in range(2)}   
            
        self.__finishingPathes = {(dispatcher, prio) :
                                  pFunc([('Running', dispatcher, prio), 'Target']) 
                                  for dispatcher in range(2) for prio in range(3)}
        
        self.__transferPathes = [pFunc([('Ressource', 0, res), ('Ressource', 1, res)]) for res in range(2)]
        
        highPrioColor = 'red3'
        midPrioColor = 'yellow3'
        lowPrioColor = 'green3'
        
        self.__prioColor = [highPrioColor, midPrioColor, lowPrioColor]
        
        idleColor = 'yellow'
        activeColor = 'green'
        cancelColor = 'orangered'
        steelColor = 'orchid'
        stallColor = 'red'
        
        self.__car = pg.image.load("Media/Car.png")
        self.__ambulance = pg.image.load("Media/Ambulance.png")
        self.__depot = pg.image.load("Media/Diamond.png")
        
        callImage = pg.image.load("Media/Call.png")
        self.__callImages = [Sprite.GetColorizedSprite(callImage, highPrioColor),
                             Sprite.GetColorizedSprite(callImage, midPrioColor),
                             Sprite.GetColorizedSprite(callImage, lowPrioColor)
                             ]
        
        slotImage = pg.image.load("Media/Frame.png")
        self.__finalImage = slotImage
        self.__slotImages = [Sprite.GetColorizedSprite(slotImage, highPrioColor),
                             Sprite.GetColorizedSprite(slotImage, midPrioColor),
                             Sprite.GetColorizedSprite(slotImage, lowPrioColor)
                             ]
        
        actorImage = pg.image.load("Media/Circle.png")
        
        self.__actorImages = [Sprite.GetColorizedSprite(actorImage, idleColor),
                             Sprite.GetColorizedSprite(actorImage, activeColor),
                             Sprite.GetColorizedSprite(actorImage, cancelColor),
                             Sprite.GetColorizedSprite(actorImage, steelColor),
                             Sprite.GetColorizedSprite(actorImage, stallColor)
                             ]
            
                             
        self.__backGround = Sprite.GetHDBackground('Black')
        self.__timePaint = Continuos.ContinuousBar(5, 120, 1080, 'Grey', 'Blue', 2)
        self.__font = pg.font.SysFont(None, 32)
        
        
                                                 
        
    
    @property
    def ImageSize(self):
        '''
        Returns the size of the background image and therefore the video

        Returns
        -------
            Pair of width and height of the desired video.

        '''
        return (1920,1080)
        
        
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
        
        points = self.__pointCollection.GetPoint
        # First background
        surface.blit(self.__backGround, (0,0))
        # Draw the exit point.
        Sprite.PaintSprite(surface, self.__finalImage,points('Target'))
        
        
        # Now we draw all static parts
        for actor, info in situations.items():
            match actor:
                case 'LastTime':
                    Sprite.PrintText(surface, f"T:{(info['Info'] / 60):.2f}", self.__font, points('Time'))
                case ('InCall', prio):
                    position = points(('InCall', prio))
                    Sprite.PaintSprite(surface, self.__slotImages[prio], position)
                    Sprite.PrintText(surface, f"{info['Info']}", self.__font, position)
                case ('ToDispatch', dispatcher, prio):
                    position = points(('Dispatched', dispatcher, prio))
                    Sprite.PaintSprite(surface, self.__slotImages[prio], position)
                    Sprite.PrintText(surface, f"{info['Info']}", self.__font, position)
                case ('Running', dispatcher, prio):
                    position = points(('Running', dispatcher, prio))
                    Sprite.PaintSprite(surface, self.__slotImages[prio], position)
                    Sprite.PrintText(surface, f"{info['Info']}", self.__font, position)
                case ('Ressource', dispatcher, ressource):
                    position = points(('Ressource', dispatcher, ressource))
                    Sprite.PaintSprite(surface, self.__depot, position)
                    Sprite.PrintText(surface, f"{info['Info']}", self.__font, position)
                case ('CallTaker', taker):
                    position = points(('Taker', taker))
                    match info['Info']:
                        case 'Idle':
                            image = self.__actorImages[0]
                        case 'Stalled':
                            image = self.__actorImages[4]
                        case ('Taking', _ , _):
                            image = self.__actorImages[1]
                    Sprite.PaintSprite(surface, image, position)
                case ('Dispatcher', dispatcher):
                    position = points(('Dispatcher', dispatcher))
                    match info['Info']:
                        case 'Idle':
                            image = self.__actorImages[0]
                        case 'Stalled':
                            image = self.__actorImages[4]
                        case ('Dispatch', _ , _):
                            image = self.__actorImages[1]
                        case ('Cancel', _ , _):
                            image = self.__actorImages[2]
                        case ('Steal', _ ):
                            image = self.__actorImages[3]
                    Sprite.PaintSprite(surface, image, position)
                    
        time = situations['Time']['Progress']            
        self.__timePaint.paint(surface,  self.__pointCollection.GetPoint('Bar'),  time)
        
        # Now the dynamic stuff.
        interP =  Pos.PositionManager.GetInterpolatedPosition
        for actor, info in situations.items():
            progress = info['Progress']
            stat = info['Info']
            match actor:
               
                case ('CallTaker', taker):
                    if not isinstance(stat, tuple):
                        continue
                    _ , prio, dispatcher = stat
                    
                    path = self.__callTakerPathes[( prio, taker, dispatcher)]
                    Sprite.DrawLine(surface, self.__prioColor[prio], path)
                    position = interP(path, progress)
                    Sprite.PaintSprite(surface, self.__callImages[prio], position)
              
                case ('Dispatcher', dispatcher):
                    match stat:
                        case ('Dispatch', prio , requiredRessources):
                            path = self.__executionPathes[(dispatcher, prio)]
                            Sprite.DrawLine(surface, self.__prioColor[prio], path)
                            position = interP(path, progress)
                            Sprite.PaintSprite(surface, self.__callImages[prio], position)
                            if requiredRessources[0] != 0:
                                position = interP(self.__resorceAssignmentPathes[(dispatcher, prio, 0)], progress)
                                Sprite.PaintSprite(surface, self.__ambulance, position)
                            if requiredRessources[1] != 0:
                                position = interP(self.__resorceAssignmentPathes[(dispatcher, prio, 1)], progress)
                                Sprite.PaintSprite(surface, self.__car, position)
                        case ('Cancel', prio , requiredRessources):
                            path = self.__executionPathes[(dispatcher, prio)]
                            Sprite.DrawLine(surface, self.__prioColor[prio], path)
                            position = interP(path, 1.0 - progress)
                            Sprite.PaintSprite(surface, self.__callImages[prio], position)
                            if requiredRessources[0] != 0:
                                position = interP(self.__resorceAssignmentPathes[(dispatcher, prio, 0)], 1.0 - progress)
                                Sprite.PaintSprite(surface, self.__ambulance, position)
                            if requiredRessources[1] != 0:
                                position = interP(self.__resorceAssignmentPathes[(dispatcher, prio, 1)], 1.0 - progress)
                                Sprite.PaintSprite(surface, self.__car, position)
                        case ('Steal', res):
                            image = self.__ambulance if res == 0 else self.__car
                            interPol = progress if dispatcher == 1 else 1.0 - progress
                            Sprite.DrawLine(surface, 'White', self.__transferPathes[res])
                            position = interP(self.__transferPathes[res], interPol)
                            Sprite.PaintSprite(surface, image, position)
                case ('Finishing', _):
                    dispatcher = stat['Dispatcher']
                    prio = stat['Prio']
                    res = stat['Ressources']
                    # First the assignment.
                    path = self.__finishingPathes[(dispatcher, prio)]
                    Sprite.DrawLine(surface, self.__prioColor[prio], path)
                    position = interP(path, progress)
                    Sprite.PaintSprite(surface, self.__callImages[prio], position)
                    # Now the remaining ressources get returned.
                    if res[0] != 0:
                        position = interP(self.__directReturnPathes[(dispatcher, prio, 0)], progress)
                        Sprite.PaintSprite(surface, self.__ambulance, position)
                    if res[1] != 0:
                        position = interP(self.__directReturnPathes[(dispatcher, prio, 1)], progress)
                        Sprite.PaintSprite(surface, self.__car, position)
                            
        
        
        # self.__pointCollection.DebugDraw(surface)
       
               
        
      
    