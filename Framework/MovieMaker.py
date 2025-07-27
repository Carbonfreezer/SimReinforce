# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 12:58:52 2025

@author: Luerig
"""


import pygame as pg
import Framework.ScriptGenerator as ScriptGenerator

import moviepy.video.VideoClip as Video

class MovieMaker:
    def __init__(self, painterGenerator):
        pg.init()
        self.__painter = painterGenerator()
        
        
        
    def __makeFrame(self, time):
        self.__painter.DrawStaticParts(self.__drawingSurface)
        self.__painter.DrawElements(self.__drawingSurface,
                                    self.__script.GetAllInterpolatedEntries(time))
        self.__painter.DrawFinalOverlay(self.__drawingSurface)  
        # Convert to numpy array
        array = pg.surfarray.array3d(self.__drawingSurface)
        array = array.swapaxes(0, 1)
        return array     
    
    
   
        
        
    def MakeMovie(self, movieFilename, scriptFilename, fps, timeScale):
        self.__script = ScriptGenerator.ScriptGenerator.LoadScript(scriptFilename+'.pkl')
        self.__timeScale = timeScale
        self.__drawingSurface = pg.Surface(self.__painter.ImageSize)
        deltaTime = timeScale / fps
        amounOfFrames = int(self.__script.MaxTime / deltaTime)
        dataList = [frame * deltaTime for frame in range(amounOfFrames)]
        clip = Video.DataVideoClip(dataList, self.__makeFrame, fps)
        clip.write_videofile(movieFilename + ".mp4", codec='libx264')
        