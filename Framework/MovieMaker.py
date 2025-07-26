# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 12:58:52 2025

@author: Luerig
"""


# pip uninstall moviepy
# pip install moviepy==1.0.3

import pygame as pg
import Framework.ScriptGenerator as ScriptGenerator

import moviepy.editor as mp

class MovieMaker:
    def __init__(self, painterGenerator):
        pg.init()
        self.__painter = painterGenerator()
        
        
        
    def __makeFrame(self, time):
        """Generate a frame at time t (in seconds)"""
       
        simulationTime = time * self.__timeScale
        self.__painter.DrawStaticParts(self.__drawingSurface)
        
        # Ask our script.
        situation = self.__script.GetAllInterpolatedEntries(simulationTime)
        self.__painter.DrawElements(self.__drawingSurface, situation)
        
            
        self.__painter.DrawFinalOverlay(self.__drawingSurface)  
        # Convert to numpy array
        array = pg.surfarray.array3d(self.__drawingSurface)
        array = array.swapaxes(0, 1)
        return array     
        
    def MakeMovie(self, movieFilename, scriptFilename, fps, timeScale):
        self.__script = ScriptGenerator.ScriptGenerator.LoadScript(scriptFilename+'.pkl')
        self.__timeScale = timeScale
        movieTime = self.__script.MaxTime / timeScale
        self.__drawingSurface = pg.Surface(self.__painter.ImageSize)
        clip = mp.VideoClip(self.__makeFrame, duration=movieTime)
        clip.fps = fps
        clip.write_videofile(movieFilename + ".mp4", codec='libx264')
        