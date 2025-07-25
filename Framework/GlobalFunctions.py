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
import Framework.MovieMaker as Movie



from sb3_contrib.common.maskable.utils import get_action_masks


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



def GenerateScript(modelSaveName, scriptName,  generator, optionalArgs = {}):
    '''
    Generates a script that can be transformed into a movie later on.

    Parameters
    ----------
    modelSaveName : TYPE
        The save name of the model.
    scriptName : TYPE
        The savename of the script without extension.
    generator : TYPE
        The generator used in the gym.
    optionalArgs : TYPE, optional
        Optional arguments for the generator.. The default is {}.

    Returns
    -------
    None.

    '''
    env = Frame.FrameworkGym(generator = generator, generateMovieScript=True, additionalOptions=optionalArgs)
    model = MaskablePPO.load(modelSaveName,  env=env)

    env = model.get_env()
    obs = env.reset()
    terminated = False
    while not terminated:
        action_masks = get_action_masks(env)
        action, _state = model.predict(obs, deterministic=True, action_masks=action_masks)
        obs, reward, terminated, info = env.step(action)
     
       
    info[0]['Script'].SaveScript(scriptName+".pkl")    
    
def GenerateMovieFromScript(scriptFilename, movieFilename, painterGenerator, fps, timeScale):
    '''
    Generates a movie from the previously generated script.

    Parameters
    ----------
    scriptFilename : TYPE
        The filename of the script.
    movieFilename : TYPE
        The movie filename we generate.
    painterGenerator : TYPE
        The class for the specific painting job.
    fps : TYPE
        The fps with which we render.
    timeScale : TYPE
        Time scale > 1 video is showing things faster than in reality.

    Returns
    -------
    None.

    '''
    movie = Movie.MovieMaker(painterGenerator)
    movie.MakeMovie(movieFilename, scriptFilename, fps, timeScale)