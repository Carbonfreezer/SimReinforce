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
        '''
        Generates the movie maker.

        Parameters
        ----------
        painterGenerator :  
            The implemeented painting plugin to paint the scene.

        Returns
        -------
        None.

        '''
        
        pg.init()
        self.__painter = painterGenerator()
        
          
    def __makeFrame(self, time):
        '''
        Callback to generate an image for a certain time step.

        Parameters
        ----------
        time :  
            The time to generate the image for.

        Returns
        -------
         
            Generated image as numpy array.

        '''
        return self.__createImageFromData(self.__script.GetAllInterpolatedEntries(time))
      
    
    def __createImageFromData(self, data):
        '''
        Creates an image from a data set.

        Parameters
        ----------
        data :  
            The data set is a dictionary associating the name of an actor with another dictionary.
            This dictionary has the entries 'Progress' which is s float between [0,1] 
            and can be used to map the situation to a continuous change, and an entry 'Info' which is arbitrary data
            from the logging system.

        Returns
        -------
        array :  
            Numpy array of image.

        '''
        self.__painter.DrawScene(self.__drawingSurface, data)
        # Convert to numpy array
        array = pg.surfarray.array3d(self.__drawingSurface)
        array = array.swapaxes(0, 1)
        return array   
    
        
    def MakeMovie(self, movieFilename, logList, fps, timeScale):
        '''
        Generates a movie from a list of log entries.

        Parameters
        ----------
        movieFilename :  
            The filename (without .mp4) of the movie file we generate.
        logList :  
            The list of the log entries to generate a movie from.
        fps :  
            The frames per second of the movie.
        timeScale :  
            Time multiplication factor for the movie >1 means movie is faster then reality.

        Returns
        -------
        None.

        '''
        self.__script = ScriptGenerator.ScriptGenerator(logList=logList)
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
        