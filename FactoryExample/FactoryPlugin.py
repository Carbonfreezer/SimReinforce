# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 14:08:55 2025

@author: Luerig
"""

import gymnasium as gym
import simpy
import Framework.ScriptGenerator as Movie

class FactoryPlugin:
    
    MaxFillingInStation = 10
    
    TransferTime = [[0.0, 4.0, 4.0, 8.0], 
                    [4.0, 0.0, 1.0, 4.0], 
                    [4.0, 1.0, 0.0, 4.0],
                    [8.0, 4.0, 4.0, 0.0]
                    ]
    
    '''Contains the transfer times from yource to destination station'''
    
    def __init__(self, generatesMovie):
        self.__generatesMovie = generatesMovie

      
    
    @property
    def ActionArray(self):
        '''
            he amount of actors the environment support. Every action for every worker.
            Here for every worker processing, going to station 1,2,3,4

        Returns
        -------
        list
            Number of acions that every worker can perform.

        '''
       
        return [5,5]
    
    
    @property
    def Terminated(self):
        return self.__env.now > 1000 # We termiate after 1000
    
    @property
    def TimeOut(self):
        '''
        Gives the time out used for deadlock detection.

        Returns
        -------
        float
            Float time for deadlock detection.

        '''
        return 50.0
    
    @property
    def TimeOutPenalty(self):
        '''
        Gives the reward for the case that we run in a timeout and therefore probably a deadlock.
        Should be calibrated in relation to the rest of the reward.

        Returns
        -------
        TYPE
            penalty for dedalock.

        '''
        return -10.0
    
    @property 
    def MovieScript(self):
        '''
        Gets the movie script used to generate a movie.

        Returns
        -------
        Type
            The movie script also closes the movie script.

        '''
        
        assert self.__generatesMovie, "We must be in movie generation mode."
        return self.__movie
    
    
    def GetObservationSpace(self):
        '''
        Gets the observation space in For OpenAi gym wrapppers.

        Returns
        -------
        dict
            The observation space.

        '''
        return {'Filling A': gym.spaces.Discrete(FactoryPlugin.MaxFillingInStation + 1),
                'Filling B': gym.spaces.Discrete(FactoryPlugin.MaxFillingInStation + 1),
                # 4: Beeing at station 1,2,3,4 4: Transition to station 1,2,3,4
                'Worker 1' : gym.spaces.Discrete(8),
                'Worker 2' : gym.spaces.Discrete(8)
                }
    
    
    def PrepareAction(self, actorChosen, localAction):
        '''
        Does all immediate prerations for the action to avoid masking conflicts..

        Parameters
        ----------
        actorChosen : TYPE
            The actor that performs the action.
        localAction : TYPE
            The action done on that actor.

        Returns
        -------
        None.

        '''
        
       
        if localAction != 0:
            source = self.__workerAtOrGoingToStation[actorChosen]
            destination = localAction - 1
            self.__stationOccupied[source] = False
            self.__stationOccupied[destination] = True
        
    
    def PerformAction(self, actorChosen, localAction):
        '''
        Performs an action of the chosen actor with the indicated index of the action of that specific actor.

        Parameters
        ----------
        actorChosen : TYPE
            The actor that performs the action.
        localAction : TYPE
            The action done on that actor.

        Returns
        -------
        None.

        '''
      
        actorCode = f"A{actorChosen}"
        
        # In this case we are working
        if localAction == 0:
            if self.__generatesMovie:
                self.__movie.AddAction(actorCode, 
                                      {'State': 'Working' , 
                                       'Station' : self.__workerAtOrGoingToStation[actorChosen]})
            self.__workerCurrentlyInTransfer[actorChosen] = False
            # Check if we are at the first station.
            if self.__workerAtOrGoingToStation[actorChosen] == 0:
                yield self.__env.timeout(5.0) # We work 5 seconds at station 0
                yield self.__fillingOfDepot[0].put(1) # We fill in 1 unit in depot 1
                if self.__generatesMovie:
                    self.__movie.AddAction( 'DA',  self.__fillingOfDepot[0].level)
                self.__rewward += 0.01 # We add a small reward for doing a first processing step.
            elif self.__workerAtOrGoingToStation[actorChosen] in [1,2]:
                # The other two stations transfer 1 unit.
                yield self.__fillingOfDepot[0].get(1) # Get 1 unit.
                if self.__generatesMovie:
                    self.__movie.AddAction( 'DA',  self.__fillingOfDepot[0].level)
                yield self.__env.timeout(10.0) # Work for 10 seconds.
                yield self.__fillingOfDepot[1].put(1) # Fills into the second depot.
                if self.__generatesMovie:
                    self.__movie.AddAction('DB',  self.__fillingOfDepot[1].level)
                self.__rewward += 0.01 # Get a small reward.
            else: # This must be the last station (3)
                assert self.__workerAtOrGoingToStation[actorChosen] == 3, "This should be station 3"
                yield self.__fillingOfDepot[1].get(1) # Get 1 unit.
                if self.__generatesMovie:
                    self.__movie.AddAction('DB',  self.__fillingOfDepot[1].level)
                yield self.__env.timeout(5.0) # We work 5 seconds 
               
                self.__rewward += 0.98 # Get finsh reward.
        else:
            # Here we are going to a station.
            self.__workerCurrentlyInTransfer[actorChosen] = True
            destination = localAction - 1
            currentStation = self.__workerAtOrGoingToStation[actorChosen]
            self.__workerAtOrGoingToStation[actorChosen] = destination
            time = FactoryPlugin.TransferTime[currentStation][destination]
            if self.__generatesMovie:
                self.__movie.AddAction( actorCode, 
                                      {'State': 'Walking' , 
                                       'Station' : currentStation,
                                       'Destination' : destination})
                
            yield self.__env.timeout(time)
            
    
    
    def action_masks(self, actorChosen):
        '''
        Gives the action mask for the chosen actor.

        Parameters
        ----------
        actorChosen : TYPE
            The actor we want to get the mask for.

        Returns
        -------
        TYPE
            Array with the indication which actions are legal in the current situation.

        '''


        # We can always work but we can not go to a station that is currently occupied.       
        result = [True] + [not x for x in self.__stationOccupied]
        return result
    
    def GetAndResetReward(self):
        '''
        Asks for the accumulated reward and resets it.

        Returns
        -------
        accReward : TYPE
            Returns accumulated reward.

        '''
        accReward = self.__rewward
        self.__rewward = 0.0
        return accReward
    
        
    def reset(self, simPyEnv, randGen):
        '''
        Resets the environment

        Parameters
        ----------
        simPyEnv : TYPE
            The simpy environment we use for simulation. This is atumatically refreshed on every reset.
        randGen : TYPE
            The random number generator for the environment

        '''
        
        self.__rewward = 0.0
        self.__env = simPyEnv
        
        if self.__generatesMovie:
            self.__movie = Movie.ScriptGenerator(simPyEnv)
            self.__movie.AddAction( 'DA', 0)
            self.__movie.AddAction( 'DB', 0)
            self.__movie.AddAction( 'A0', {'State': 'Working' , 'Station' : 0})
            self.__movie.AddAction( 'A1', {'State': 'Working' , 'Station' : 1})
        
        
        
        self.__workerCurrentlyInTransfer = [False, False]
        '''Flags if the worker is currently moving'''
        self.__workerAtOrGoingToStation = [0, 1]
        '''Flags where the worker is currently at or moving to'''
        self.__fillingOfDepot = [simpy.Container(simPyEnv, capacity = FactoryPlugin.MaxFillingInStation),
                                 simpy.Container(simPyEnv, capacity = FactoryPlugin.MaxFillingInStation)
                                 ] 
        '''Contains the filling of the current depot'''
        self.__stationOccupied = [True, True, False, False]
        '''Contains the information if the station is currently occupied'''
        
      
        
    def GetObservation(self):
        '''
        Function that generates the current observation.

        Returns
        -------
        dict
            Observation dictionary.

        '''
        return {'Filling A' : self.__fillingOfDepot[0].level,
                'Filling B' : self.__fillingOfDepot[1].level,
                'Worker 1': self.__workerAtOrGoingToStation[0] + 
                    (4 if self.__workerCurrentlyInTransfer[0] else 0),
                'Worker 2' :   self.__workerAtOrGoingToStation[1] + 
                    (4 if self.__workerCurrentlyInTransfer[1] else 0)   
                    }