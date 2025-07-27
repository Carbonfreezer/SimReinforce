# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 12:58:52 2025

@author: Luerig
"""


import pygame as pg
import Framework.ScriptGenerator as ScriptGenerator

import moviepy.video.VideoClip as Video
import moviepy.video.compositing as comp

class MovieMaker:
    def __init__(self, painterGenerator):
        pg.init()
        self.__painter = painterGenerator()
        
        
        
    def __makeFrame(self, time):
        return self.__createImageFromData(self.__script.GetAllInterpolatedEntries(time))
      
    
    def __createImageFromData(self, data):
        self.__painter.DrawScene(self.__drawingSurface, data)
        # Convert to numpy array
        array = pg.surfarray.array3d(self.__drawingSurface)
        array = array.swapaxes(0, 1)
        return array   
    
        
    def MakeMovie(self, movieFilename, logList, fps, timeScale):
        self.__script = ScriptGenerator.ScriptGenerator(logList=logList)
        self.__timeScale = timeScale
        self.__drawingSurface = pg.Surface(self.__painter.ImageSize)
        deltaTime = timeScale / fps
        amounOfFrames = int(self.__script.MaxTime / deltaTime)
        dataList = [frame * deltaTime for frame in range(amounOfFrames)]
        movie = Video.DataVideoClip(dataList, self.__makeFrame, fps)
        # Now we add header and trailer
        header = Video.ImageClip(self.__makeFrame(0.0), duration=1.0)
        trailer = Video.ImageClip(self.__createImageFromData(self.__script.GetLastState()), duration=1.0) 
        clip = comp.CompositeVideoClip.concatenate_videoclips([header, movie, trailer])
        clip.write_videofile(movieFilename + ".mp4", codec='libx264')
        