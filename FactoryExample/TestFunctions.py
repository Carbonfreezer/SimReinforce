# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 09:13:43 2025

@author: Luerig
"""

import FactoryExample.FactoryPlugin as FactoryPlugin
import Framework.GlobalFunctions as Global

import FactoryExample.FactoryPainter as Painter

#Global.PerformTraining("MyBestModel", FactoryPlugin.FactoryPlugin)

#Global.GenerateScript("MyBestModel", "ScriptForModel",  FactoryPlugin.FactoryPlugin)


Global.GenerateMovieFromScript("ScriptForModel", "Process", Painter.FactoryPainter, 30, 10.0)

