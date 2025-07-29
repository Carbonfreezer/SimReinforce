# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 07:49:26 2025

@author: Luerig
"""

from  CashierExample import CashierSimulator
import Framework.GlobalFunctions as Global

import CashierExample.CashierPainter as Painter








Global.PerformTraining("SmartModel", CashierSimulator.CashierSimulator,
                       optionalArgs={'usesAutoDispatcher': False},
                        sizeOfMacroBatch=20_000, 
                         evaluationRuns=100, macroBatches=30, numOfParallelEnvs = 2,
                        additionalPPOargs = {'gamma' : 1.0, 'ent_coef' : 0.05})



Global.GenerateMovie("SmartMovie", "SmartModel",   CashierSimulator.CashierSimulator,  Painter.CashierPainter, 30, 5.0, 
                     randomSeed=0, optionalArgsGym={'usesAutoDispatcher': False} )


         
Global.PerformTraining("AutoModel", CashierSimulator.CashierSimulator,
                       optionalArgs={'usesAutoDispatcher': True},
                        sizeOfMacroBatch=20_000, 
                         evaluationRuns=100, macroBatches=30, numOfParallelEnvs = 2,
                        additionalPPOargs = {'gamma' : 1.0, 'ent_coef' : 0.05})



Global.GenerateMovie("AutoMovie", "AutoModel",   CashierSimulator.CashierSimulator,  Painter.CashierPainter, 30, 5.0, 
                     randomSeed=0, optionalArgsGym={'usesAutoDispatcher': True} )

