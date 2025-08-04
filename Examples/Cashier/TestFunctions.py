# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 07:49:26 2025

@author: Luerig
"""

import sys
sys.path.insert(0, '../..')


import Framework.GlobalFunctions as Global

from  Examples.Cashier import Simulator
from Examples.Cashier import Painter



if __name__ == '__main__':
    
    Global.PerformTraining("SmartModel", Simulator.Simulator,
                           optionalArgs={'usesAutoDispatcher': False},
                            sizeOfMacroBatch=20_000, 
                             evaluationRuns=1000, macroBatches=30, numOfParallelEnvs = 2
                            )
    
    
    
    Global.GenerateMovie("SmartMovie", "SmartModel",   Simulator.Simulator,  
                         Painter.Painter, 30, 5.0, 
                         randomSeed=0, optionalArgsGym={'usesAutoDispatcher': False} )
    
    
             
    Global.PerformTraining("AutoModel", Simulator.Simulator,
                           optionalArgs={'usesAutoDispatcher': True},
                            sizeOfMacroBatch=20_000, 
                             evaluationRuns=1000, macroBatches=30, numOfParallelEnvs = 2
                            )
    
    
    
    Global.GenerateMovie("AutoMovie", "AutoModel",   Simulator.Simulator,  
                         Painter.Painter, 30, 5.0, 
                         randomSeed=0, optionalArgsGym={'usesAutoDispatcher': True} )

