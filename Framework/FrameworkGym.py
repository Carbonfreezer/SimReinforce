# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 14:02:19 2025

@author: Luerig
"""

import gymnasium as gym
import simpy
from simpy.events import AnyOf



class FrameworkGym(gym.Env):
      
    def __init__(self, generator, generateMovieScript=False, additionalOptions={}):
        '''
        Generates the gmy in OpenAI gym format.

        Parameters
        ----------
        generator : TYPE
            DESCRIPTION. The class name of the concrete implementation.
        generateMovieScript : TYPE, optional
            DESCRIPTION. Indicates if we want to generate a movie script, default is false
        additionalOptions : TYPE, optional
            DESCRIPTION. additional parameters to generate the internal gym.

        Returns
        -------
        None.

        '''
        
        self.__plugin = generator(generateMovieScript, **additionalOptions)
        self.__numActors =  len(  self.__plugin.ActionArray)
        self.__generateMovieScript = generateMovieScript
        baseObservationSpace =  self.__plugin.GetObservationSpace()
        # We add the actor who is going to act next as observation.
        baseObservationSpace['Actor'] = gym.spaces.Discrete(self.__numActors)
        self.observation_space = gym.spaces.Dict(baseObservationSpace)
        self.action_space = gym.spaces.Discrete(sum(  self.__plugin.ActionArray)) 
      
        

    def reset(self, seed = None, options = None):
        '''
        The reset function in the open AI gym format.

        Parameters
        ----------
        seed : TYPE, optional
            DESCRIPTION. The seed for the random number generator.
        options : TYPE, optional
            DESCRIPTION. Additional ooptions

        Returns
        -------
        TYPE
            The observations after reset.
        dict
            Optinal information empty here.

        '''
        super().reset(seed=seed)
        self.__env = simpy.Environment()
        self.__actorsWaitingForCommand = list(range(self.__numActors))
        self.__actorEvents = [None] * self.__numActors
        self.__plugin.reset(self.__env, super().np_random)
        return self.__get_obs(), {}
   
    
    def __getLocalAction(self, action, actorToChoose):
        '''
        Gets the action for a specific actor from the general action number.

        Parameters
        ----------
        action : TYPE
            The general action number
        actorToChoose : TYPE
            The we want to get the action for.

        Returns
        -------
        TYPE
            The actor specific action.

        '''
        baseSum = sum(self.__plugin.ActionArray[:actorToChoose])
        return int(action) - baseSum
    
    def __get_obs(self):
        '''
        Gets thhe current observation

        Returns
        -------
        observation : TYPE
            Complete observation with active actor.

        '''
        observation = self.__plugin.GetObservation()       
        # In the case we have run into the timeout, we still need to flag an actor as part of the observation.
        observation['Actor'] =  0 if not self.__actorsWaitingForCommand else  self.__actorsWaitingForCommand[0]
        return observation
    
    def step(self, action):
        '''
        Step function for the Open AI gym-

        Parameters
        ----------
        action : TYPE
            The global chosen action.

        Returns
        -------
        observation : TYPE
            The observation of the situation.
        reward : TYPE
            Reward gotten on action.
        isTerminated : TYPE
            Are we terminated.
        bool
            Always false for truncated.
        infoDir : TYPE
            Contains the movie script if required and if sepisode terminated,.

        '''
        currentActor = self.__actorsWaitingForCommand.pop(0)
        actorSpecificAction = self.__getLocalAction(action, currentActor)
        # Because the process is just kicked off at the next run, we have to eventually prepare action here 
        # immediately to avoid ay conflicts in action masking on other actors.
        self.__plugin.PrepareAction(currentActor, actorSpecificAction)
        self.__actorEvents[currentActor] = self.__env.process(self.__plugin.PerformAction(currentActor, actorSpecificAction))
        wasTimeOut = False
        # Check if we have done all, if this is the case we have to run to get the next action.
        if not self.__actorsWaitingForCommand:
            deadLockGuard = self.__env.timeout(self.__plugin.TimeOut)
            waitList = (x for x in self.__actorEvents if x )
            self.__env.run( deadLockGuard | AnyOf(self.__env, waitList))
            wasTimeOut = deadLockGuard.processed
            for idx, event in enumerate(self.__actorEvents):
                if event and event.processed:
                    self.__actorsWaitingForCommand.append(idx)
                    self.__actorEvents[idx] = None
                    
        reward = self.__plugin.TimeOutPenalty if wasTimeOut else self.__plugin.GetAndResetReward()
        observation = self.__get_obs()
        isTerminated = self.__plugin.Terminated or wasTimeOut
        infoDir = {}
        if isTerminated and self.__generateMovieScript:
            infoDir['Script'] = self.__plugin.MovieScript.LogList
        return observation, reward, isTerminated, False, infoDir

            

    def action_masks(self):
        '''
        Gets the action mask for the current situation.

        Returns
        -------
        res : TYPE
            Array with valid actions.

        '''
        currentActor = self.__actorsWaitingForCommand[0]
        header = sum( self.__plugin.ActionArray[:currentActor])
        trailer = sum(  self.__plugin.ActionArray[currentActor + 1:])
        localMask = self.__plugin.action_masks(self.__actorsWaitingForCommand[0])
        res = [False] * header+ localMask + [False] * trailer
        return res



# gym.register("gymnasium/Processing", entry_point=FrameworkGym)
   

