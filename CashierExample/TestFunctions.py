# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 07:49:26 2025

@author: Luerig
"""

from  CashierExample import CashierSimulator
import Framework.GlobalFunctions as Global

import CashierExample.CashierPainter as Painter


         
Global.PerformTraining("TestModel", CashierSimulator.CashierSimulator,sizeOfMacroBatch=20_000, 
                         evaluationRuns=100, macroBatches=5, numOfParallelEnvs = 2,
                        additionalPPOargs = {'gamma' : 1.0, 'ent_coef' : 0.05})



Global.GenerateMovie("TestMovie", "TestModel", CashierSimulator.CashierSimulator,  Painter.CashierPainter, 30, 5.0, 
                     randomSeed=0 )

