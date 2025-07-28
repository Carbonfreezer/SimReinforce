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
from stable_baselines3.common.env_util import make_vec_env


def PerformTraining(modelSaveName, generator, optionalArgs = {}, additionalPPOargs={}, numOfParallelEnvs = 1,
                    macroBatches = 5, sizeOfMacroBatch = 100_000, evaluationRuns = 1000):
    '''
    Performs a training of the Maskakble PPO model.

    Parameters
    ----------
    modelSaveName :  
        The filename, where the model should get saved to.
    generator :  
        The generator class for the specific Gym.
    optionalArgs :  , optional
        Optional args for the gym generator. The default is {}.
    additionalPPOargs :  , optional
        additional args for the Mskable PPO trainer. The default is {}.
    numOfParallelEnvs:  , optional
        The number of environments we want to run in parallel. Depends on the amount of CPUs you have. The default is 1.
    macroBatches :  , optional
        The number of macro batches used in training. The default is 5.
    sizeOfMacroBatch :  , optional
        The number of episodes generated per macro batch. The default is 100_000.
    evaluationRuns :  , optional
        The number of evaluation runs executed after macro batch. The default is 1000.

    Returns
    -------
    None.

    '''
    
    
    if numOfParallelEnvs == 1:
        env = Frame.FrameworkGym(generator = generator, generateMovieScript=False, additionalOptions=optionalArgs)
    else:
        env = make_vec_env(lambda : Frame.FrameworkGym(generator = generator, generateMovieScript=False, additionalOptions=optionalArgs), 
                           n_envs= numOfParallelEnvs)
        
    test_env = Frame.FrameworkGym(generator = generator, generateMovieScript=False, additionalOptions=optionalArgs)  
    
    model = MaskablePPO("MultiInputPolicy", env, **additionalPPOargs)
    
   
    evalCallback = MaskableEvalCallback( eval_env=test_env, 
                                        callback_on_new_best = Custom.CustomEvalCallback(modelSaveName),
                                        eval_freq=sizeOfMacroBatch / numOfParallelEnvs,
                                        n_eval_episodes=evaluationRuns)
    
    model.learn(total_timesteps=macroBatches * sizeOfMacroBatch, callback=evalCallback)



def GenerateMovie(movieFilename, modelName, gymGenerator, painterGenerator, fps, timeScale, optionalArgsGym = {}):
    '''
    Generates a movie from a trained model.

    Parameters
    ----------
    movieFilename : 
        The movie filename without extension (will be .mp4)
    modelName : 
        The name of the model we load to generate the movie.
    gymGenerator : 
        The implemented generator class for the gym.
    painterGenerator : 
        The implemented visualizer class of the systemn.
    fps :
        frames per second for the movie.
    timeScale : 
        time scale for movie and simulation, if larger one movie is shorter than reality.
    optionalArgsGym :  optional
        Optional arguments for the generator gym class. The default is {}.

    Returns
    -------
    None.

    '''
    env = Frame.FrameworkGym(generator = gymGenerator, generateMovieScript=True, additionalOptions=optionalArgsGym)
    model = MaskablePPO.load(modelName,  env=env)

    env = model.get_env()
    obs = env.reset()
    terminated = False
    while not terminated:
        action_masks = get_action_masks(env)
        action, _state = model.predict(obs, deterministic=True, action_masks=action_masks)
        obs, reward, terminated, info = env.step(action)
        
        
    movieScript = info[0]['Script']
    
   
    movie = Movie.MovieMaker(painterGenerator)
    movie.MakeMovie(movieFilename, movieScript, fps, timeScale)    
    
    
