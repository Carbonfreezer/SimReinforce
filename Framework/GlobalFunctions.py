# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 08:45:45 2025

Contains some global helper functions.

@author: Luerig
"""

from sb3_contrib import MaskablePPO
import Framework.CustomEvalCallback as Custom
from sb3_contrib.common.maskable.callbacks import MaskableEvalCallback


import Framework.FrameworkGym as Frame


def PerformTraining(modelSaveName, generator, optionalArgs = {}, additionalPPOargs={},
                    macroBatches = 5, sizeOfMacroBatch = 100_000, evaluationRuns = 1000):
    '''
    Performs a training of the Maskakble PPO model.

    Parameters
    ----------
    modelSaveName : TYPE
        The filename, where the model should get saved to.
    generator : TYPE
        The generator class for the specific Gym.
    optionalArgs : TYPE, optional
        Optional args for the gym generator. The default is {}.
    additionalPPOargs : TYPE, optional
        additional args for the Mskable PPO trainer. The default is {}.
    macroBatches : TYPE, optional
        The number of macro batches used in training. The default is 5.
    sizeOfMacroBatch : TYPE, optional
        The number of episodes generated per macro batch. The default is 100_000.
    evaluationRuns : TYPE, optional
        The number of evaluation runs executed after macro batch. The default is 1000.

    Returns
    -------
    None.

    '''
    
    env = Frame.FrameworkGym(generator = generator, generateMovieScript=False, additionalOptions=optionalArgs)
    model = MaskablePPO("MultiInputPolicy", env, **additionalPPOargs)
    
   
    evalCallback = MaskableEvalCallback( eval_env=env, 
                                        callback_on_new_best = Custom.CustomEvalCallback(modelSaveName),
                                        eval_freq=sizeOfMacroBatch,
                                        n_eval_episodes=evaluationRuns)
    
    model.learn(total_timesteps=macroBatches * sizeOfMacroBatch, callback=evalCallback)

