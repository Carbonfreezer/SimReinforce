# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 09:13:43 2025

@author: Luerig
"""

import FactoryExample.FactoryPlugin as FactoryPlugin
import Framework.GlobalFunctions as Global

import FactoryExample.FactoryPainter as Painter


Global.PerformTraining("TestModel", FactoryPlugin.FactoryPlugin,sizeOfMacroBatch=20_000, 
                       evaluationRuns=1, macroBatches=30, numOfParallelEnvs = 2,
                       additionalPPOargs = {'gamma' : 1.0, 'ent_coef' : 0.05})
Global.GenerateMovie("TestMovie", "TestModel", FactoryPlugin.FactoryPlugin,  Painter.FactoryPainter, 30, 5.0 )


