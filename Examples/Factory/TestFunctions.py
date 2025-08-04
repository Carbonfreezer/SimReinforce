# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 09:13:43 2025

@author: Luerig
"""


import sys
sys.path.insert(0, '../..')

import Framework.GlobalFunctions as Global

from  Examples.Factory import Simulator
from Examples.Factory import Painter


Global.PerformTraining("TestModel", Simulator.Simulator,sizeOfMacroBatch=20_000, 
                       evaluationRuns=1, macroBatches=30, numOfParallelEnvs = 2,
                       additionalPPOargs = {'gamma' : 1.0, 'ent_coef' : 0.05})
Global.GenerateMovie("TestMovie", "TestModel", Simulator.Simulator,  Painter.Painter, 30, 5.0 )


