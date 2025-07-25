# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 09:13:43 2025

@author: Luerig
"""

import FactoryPlugin
import Framework.GlobalFunctions as Global


import Framework.MovieMaker as Movie
import FactoryExample.FactoryPainter as Painter
import pygame as pg
import Framework.PositionExtractor as PosExtract

#Global.PerformTraining("MyBestModel", FactoryPlugin.FactoryPlugin)
#Global.GenerateScript("MyBestModel", "ScriptForModel",  FactoryPlugin.FactoryPlugin)

movie = Movie.MovieMaker(Painter.FactoryPainter)
movie.MakeMovie("hotStuff", "ScriptForModel", 24, 20.0)

