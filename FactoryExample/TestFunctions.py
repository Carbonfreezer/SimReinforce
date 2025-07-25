# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 09:13:43 2025

@author: Luerig
"""

import FactoryPlugin
import Framework.GlobalFunctions as Global

Global.PerformTraining("TestModel", FactoryPlugin.FactoryPlugin, macroBatches=10)
#Global.GenerateScript("MyBestModel", "ScriptForModel",  FactoryPlugin.FactoryPlugin)
