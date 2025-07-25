# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 09:13:43 2025

@author: Luerig
"""

import FactoryPlugin
import Framework.GlobalFunctions as Global

import FactoryExample.FactoryPainter as Painter

#Global.PerformTraining("MyBestModel", FactoryPlugin.FactoryPlugin)
#Global.GenerateScript("MyBestModel", "ScriptForModel",  FactoryPlugin.FactoryPlugin)


Global.GenerateMovieFromScript("SCriptForModel", "Process", Painter.FactoryPainter, 24, 4.0)

