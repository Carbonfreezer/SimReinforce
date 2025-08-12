# -*- coding: utf-8 -*-
"""
Created on Sat Aug  9 14:47:54 2025

@author: chris
"""

import gymnasium as gym
import simpy
from simpy.resources.store import Store
from Framework import ScriptRecorder
from Framework.Simulation import WaitingModule
import numpy as np

import EmergencyCall
import EmergencyCallCategory

class Simulator:
    
    
    
    Categories = [EmergencyCallCategory.EmergencyCallCategory(0,10 * 60 , 1.0, 0.0, 5.0 * 60.0, 15.0*60.0, [1,1], (8.0*60, 120)),
                  # Gighest priority ambulance and emergency car.
                  EmergencyCallCategory.EmergencyCallCategory(1,5 * 60,  0.8, 0.2, 5.0 * 60.0, 15.0*60.0, [1,0], (8.0*60, 120)),
                  # Second highest priority with ambulance car.
                  EmergencyCallCategory.EmergencyCallCategory(2,3 * 60,  0.5, 0.3, 5.0 * 60.0, 20.0*60.0, [1,0], (12.0*60, 180)),
                  # Third highest priority with ambulance car, no emergeny signal.
                  ]
    
    '''The different emergeny call categories we can have.'''
    
    MaxFillingWaitSlots = 10
    ''' The amount of pending calls / processes we can have of each type. '''
    MaxAmountOfResources = 20
    '''The max amount of resources we can have.'''
    TotalEpisodeTimes = 60 * 60 * 3
    '''Total time in seconds we want to simulate'''    
    
    CalltakerProcessingTime = [(5 * 60, 2 * 60)] * 8
    '''Average and std deviation of processing time for any of the 8 call takers.'''
    
    
    RessourceTransferTime = (60.0, 10.0)
    '''The time needed for the dispatcher to request a ressource transfer'''
    DispatcherProcessingTime = (2.0 * 60.0, 30.0)
    '''The time the dispatcher need to dispatch a task.'''
    DispatcherCancellationTime = (60.0, 10.0)
    '''The time the dispatcher needs to cancel a task.'''
    
    RewardCallTaken = 0.01
    '''The micro reward we get when a call has been taken. '''
    
    RewardCallDispatched = 0.01
    '''The micro reward we get when a call has been dispatched.. '''
    
    
    def __init__(self, generatesMovie):
        '''
        

        Parameters
        ----------
        generatesMovie :  
            bool if we want to generate a movie

        Returns
        -------
        None.

        '''
        self.__generatesMovie = generatesMovie

      
    
    @property
    def ActionArray(self):
        '''
            We have 8 call takers, that can pass until a new call comes in, or dispatch one of the 
            low, medium or high priority calls (so 4 action options in total.)
            
            Then we have two dispatchers, that can either wait or dispatch one of the calls , cancel one of the calls,
            or request one of the resources. (so 1+2*3 + 2 = 9 actions in total.)
    
        Returns
        -------
        list
            Number of acions that every worker can perform.

        '''
       
        return [4] * 8 + [9] * 2
    
    
    @property
    def TerminationEvent(self):
        '''
        Returns the termination event for the environment

        Returns
        -------
         
            Termination event.

        '''
        return self.__terminationEvent
    
    
    @property 
    def MovieScript(self):
        '''
        Gets the movie script used to generate a movie.

        Returns
        -------
         
            The movie script.

        '''
        
        return self.__movie
    
    
    def GetObservationSpace(self):
        '''
        Gets the observation space in For OpenAi gym wrapppers.

        Returns
        -------
        dict
            The observation space.

        '''
        return {'InCalls':  gym.spaces.Box(0, Simulator.MaxFillingWaitSlots, shape=(3,), dtype =np.int32),
                'WaitForDispatch' : gym.spaces.Box(0, Simulator.MaxFillingWaitSlots, shape=(2,3), dtype =np.int32),
                'InProcessing' : gym.spaces.Box(0, Simulator.MaxFillingWaitSlots, shape=(2,3), dtype =np.int32),
                'RessourcesAvailable' : gym.spaces.Box(0, Simulator.MaxAmountOfResources, shape=(2,2), dtype =np.int32),
                'Time' : gym.spaces.Box(0.0, 1.0, shape=(1,), dtype =np.float32)
                }
    
    
    def PrepareAction(self, actorChosen, localAction):
        '''
        Does all immediate prerations for the action to avoid masking conflicts..

        Parameters
        ----------
        actorChosen :  
            The actor that performs the action.
        localAction :  
            The action done on that actor.

        Returns
        -------
        None.

        '''
        
        
        if localAction == 0:
            # In this case it is a wait command, we do not need anything.
            return
        
        if actorChosen < 8:
            # This is one of the call takers.
            self.__incomingCounter[localAction - 1] -= 1
        else:
            # In this case we have a dispatcher.
            dispatcher = actorChosen - 8
            
            if localAction in [1,2,3]:
                # In this case we process an incoming call and get the resources.
                requiredResources = Simulator.Categories[localAction - 1].NeededResources
                self.__resources[dispatcher][0] -= requiredResources[0]
                self.__resources[dispatcher][1] -= requiredResources[1]
            elif localAction > 6:
                # In this case we are relocating a resource. We take one element to do it.
                self.__resources[1 - dispatcher][localAction - 7] -= 1
                
            
    def __ProcessEmergencyRun(self, call):
        '''
        Does the process of an emergency run.

        Parameters
        ----------
        call :
            The call that gets processed during the run.

        '''        
        
        callInfo = Simulator.Categories[call.Category]
        # We wait until time is over or we get interrupted.
        yield self.__waitingModule.WaitGamma(callInfo.NeededTime) | self.cancellationToken
        
        
        # Now check, if we were cancelled.
        if self.cancellationToken.processd:
            #reinsert of call to be processed. The job has already been taken out the final que. and resources have already been reassigned.
            yield self.__callsToDisptach[call.Region][call.Category].put(call)
            self.__dispatchCounter[call.Region, call.Category] += 1
        else:
            # Return the resoures.
            requiredResources = callInfo.NeededResources
            self.__ressources[call.Region,0] += requiredResources[0]
            self.__ressources[call.Region,1] += requiredResources[1]
            # Remove call.
            self.__callsExecuting[call.Region][call.Category].remove(call)
            self.__executingCounter[call.Region, call.Category] -= 1
            # In this case we take the reward.
            totalTime = self.__env.now - call.StartTime
            self.__reward += callInfo.GetReward(totalTime)
            
        self.cancellationToken = None

            
    def PerformAction(self, actorChosen, localAction):
        '''
        Performs an action of the chosen actor with the indicated index of the action of that specific actor.

        Parameters
        ----------
        actorChosen :  
            The actor that performs the action.
        localAction :  
            The action done on that actor.

        Returns
        -------
        None.

        '''
      
        if actorChosen < 8:
            #This is the case for the call taker.
            if localAction == 0:
                # In this case we want to wait for a new call coming in.
                self.__callTakeReactivation[actorChosen] = self.__env.event()
                yield self.__callTakeReactivation[actorChosen]
                self.__callTakeReactivation[actorChosen] = None
            else:
               # In this case we take a call and send it ot hte dispatcher.
               prio = localAction - 1
               call = yield self.__callsIncoming[prio].get()
               # Do the call.
               yield self.__waitingModule.WaitGamma(Simulator.CalltakerProcessingTime[actorChosen])
               # Inset the information for the call into the correct slot.
               yield self.__callsToDisptach[call.Region][prio].put(call)
               self.__dispatchCounter[call.Region, prio] += 1
               self.__reward += Simulator.RewardCallTaken
               # Eventually we have to flag the dispatcher, if he is waiting.
               event = self.__dispatcherReactivation[call.Region]
               if  event != None and not event.processed:
                   event.succeed()
        else:
           # This is one of the dispatcher.
           dispatcher = actorChosen - 8
           if localAction == 0:
               # The waitng ccase.
               self.__dispatcherReactivation[dispatcher] = self.__env.event()
               yield self.__dispatcherReactivation[dispatcher]
               self.__dispatcherReactivation[dispatcher] = None         
           elif localAction in [1,2,3]:
               # We take an incoming call and dispatch it. The ressources have already been taken in the preparation stage.
               prio = localAction - 1
               call = yield self.__callsToDisptach[dispatcher][prio].get()
               self.__dispatchCounter[dispatcher, prio] -= 1
               
               yield self.__waitingModule.WaitGamma(Simulator.DispatcherProcessingTime)
               self.__reward += Simulator.RewardCallDispatched
               
               # Put the process away.
               self.__callsExecuting[dispatcher][prio].append(call)
               self.__executingCounter[dispatcher, prio] += 1
               call.cancellationToken = self.__env.event()
               self.__env.process(self.__ProcessEmergencyRun(call))
           elif localAction in [4,5,6]:
               # In this case we cancel a job.
               jobToCancel = self.__callsExecuting[dispatcher][localAction - 4].pop(-1)
               jobToCancel.cancellationToken.succeed()
               self.__callsExecuting[dispatcher, localAction - 4] -= 1
               yield self.__waitingModule.WaitGamma(Simulator.DispatcherCancellationTime)
               self.__reward -= Simulator.RewardCallDispatched
               
               # Get the ressources.
               requiredResources = Simulator.Categories[jobToCancel.Category].NeededResources
               self.__ressources[dispatcher,0] += requiredResources[0]
               self.__ressources[dispatcher,1] += requiredResources[1]
           else:
               # In this case we transfer ressources between dispatchers. 
               # Grabbing the resource has already been done.
               yield self.__waitingModule.WaitGamma(Simulator.RessourceTransferTime)
               self.__ressources[dispatcher,localAction - 7] += 1
            
        
      
    
    
    def action_masks(self, actorChosen):
        '''
        Gives the action mask for the chosen actor.

        Parameters
        ----------
        actorChosen :  
            The actor we want to get the mask for.

        Returns
        -------
         
            Array with the indication which actions are legal in the current situation.

        '''

        if actorChosen < 8:
            # This is one of the call takers. We can always do nothing or dispatch one of the calls, if there is one in que.
            result = [True] + [self.__incomingCounter[i] > 0 for i in range(3)]
        else:
            dispatcher = actorChosen - 8
            # We can dispatch a call, if there is a call in the que and if we have enough resources available.
            dispatachableCall = []
            for prio in range(3):
                # Is there a call to dispatch and can we dispatch it?
                if  self.__dispatchCounter[dispatcher, prio] == 0 or \
                    self.__executingCounter[dispatcher,prio] >= Simulator.MaxFillingWaitSlots :
                    dispatachableCall.append(False)
                    continue
                # Now we need to check the resources.
                requiredResources = Simulator.Categories[prio].NeededResources
                dispatachableCall.append(self.__ressources[dispatcher,0] >= requiredResources[0] and 
                                         self.__ressources[dispatcher,1] >= requiredResources[1])
            # Now we need to check the calls we can cancel.
            canceableCalls = [ self.__executingCounter[dispatcher,prio]> 0 for prio in range(3)]
            
            # Now we need to check, if we can steal resources.
            steelableResources = [self.__ressources[1 - dispatcher,0] > 0, self.__ressources[1 - dispatcher,1] > 0]
            
            result =  [True] + dispatachableCall + canceableCalls + steelableResources
       
        return result
    
    
    
    def GetAndResetReward(self):
        '''
        Asks for the accumulated reward and resets it.

        Returns
        -------
        accReward :  
            Returns accumulated reward.

        '''
        accReward = self.__reward
        self.__reward = 0.0
        return accReward
    
    
    def __spawner(self, callPrio):
        '''
        The spawner process for a certain priority.

        Parameters
        ----------
        callPrio : 
            Priority of the call we process.

        Returns
        -------
        None.

        '''
        
        while True:
            # First wait.
            yield self.__waitingModule.WaitExponential(Simulator.Categories[callPrio].AverageTimeBetweenCalls)
            # Create a new call.
            region = 0 if self.__rand.random() < 0.5 else 1
            newCall = EmergencyCall.EmergencyCall(callPrio, self.__env.now, region)
            yield self.__callsIncoming[callPrio].put(newCall)
            self.__incomingCounter[callPrio] += 1
            # Trigger waiting call takers.
            for event in self.__callTakeReactivation:
                if event != None and not event.processed:
                    event.succeed()
            
            
    
        
    def reset(self, simPyEnv, randGen):
        '''
        Resets the environment

        Parameters
        ----------
        simPyEnv :  
            The simpy environment we use for simulation. This is atumatically refreshed on every reset.
        randGen :  
            The random number generator for the environment

        '''
        
        self.__reward = 0.0
        self.__env = simPyEnv
        self.__rand = randGen
        
        self.__waitingModule = WaitingModule.WaitingModule(self.__env, randGen)
        '''The waiting module we use for passing time.'''
        
        self.__terminationEvent = self.__env.timeout(Simulator.TotalEpisodeTimes)
        '''When does the episode terminate '''
        
        self.__callTakeReactivation = [None] * 8
        '''The global reactivation event for the call taker, if they are in waiting mode. ''' 
        
        self.__dispatcherReactivation = [None] * 2
        '''The global reactivation event for the call dispatcher, if they are in waiting mode. '''
        
        self.__movie = ScriptRecorder.ScriptRecorder(simPyEnv, self.__generatesMovie)
        '''The script recorder module.'''
     
        self.__incomingCounter = np.zeros((3,), dtype = np.int32)
        '''The counter with the incoming calls. This is used for action masking and directly manipulated in the prepare call.'''
        self.__callsIncoming = [Store(simPyEnv, Simulator.MaxFillingWaitSlots),
                                Store(simPyEnv, Simulator.MaxFillingWaitSlots),
                                Store(simPyEnv, Simulator.MaxFillingWaitSlots)]
        '''The different stores with the incoming calls'''
        
        
        # Start the spawners. 
        self.__env.process(self.__spawner(0))
        self.__env.process(self.__spawner(1))
        self.__env.process(self.__spawner(2))

        self.__callsToDisptach = [[Store(simPyEnv, Simulator.MaxFillingWaitSlots) for _ in range(3)] for _ in range(2)]
        '''Dispatcher array for the different dispatcher structure [dispatcher][prioritySlot]'''
        self.__dispatchCounter = np.zeros((2,3), dtype = np.int32)
        '''Counter for the calls to be dispatched also used for observations.'''
        

        self.__callsExecuting = [[ [] for _ in range(3)] for _ in range(2)]
        '''The different calls that are currently executing. This is a list because there is only one actor accessing it [dispatcher][prioritySlot].'''    
        self.__executingCounter = np.zeros((2,3), dtype = np.int32)
        '''Counter for the calls currently executed also used for observations.'''
        
        self.__ressources = np.array( [[10,2],[10,2]], dtype = np.int32)
        '''The ressources available of every type. For every dispatcher. [dispatcher][type]'''
        
        self.__movie.AddAction( 'Time', None)
    
        
    
    
        
    
        
    def GetObservation(self):
        '''
        Function that generates the current observation.

        Returns
        -------
        dict
            Observation dictionary.

        '''
         
       
        return {
            'InCalls' : self.__incomingCounter,
            'WaitForDispatch' : self.__dispatchCounter,
            'Processing' : self.__executingCounter,
            'RessourcesAvailable' : self.__ressources,
            'Time' : [np.clip(self.__env.now / Simulator.TotalEpisodeTimes, 0.0, 1.0)]
            }
    