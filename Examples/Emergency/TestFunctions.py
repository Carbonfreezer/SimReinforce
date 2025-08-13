# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 12:24:39 2025

@author: chris
"""



import sys
sys.path.insert(0, '../..')

import Framework.GlobalFunctions as Global

from  Examples.Emergency import Simulator
from Examples.Emergency import Painter

import torch as th


if __name__ == '__main__':
    
    policy_kwargs = dict(activation_fn=th.nn.ReLU,
                     net_arch=dict(pi=[128,128], vf=[128, 128]))
    
    
    Global.PerformTraining("TestModel", Simulator.Simulator,sizeOfMacroBatch=20_000, 
                           evaluationRuns=1000, macroBatches=5, numOfParallelEnvs = 2,
                           additionalPPOargs = { 'policy_kwargs': policy_kwargs})
    Global.GenerateMovie("TestMovie", "TestModel", Simulator.Simulator,  Painter.Painter, 30, 15.0 )
    
    
