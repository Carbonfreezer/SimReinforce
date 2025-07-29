# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 13:31:53 2025

@author: Luerig
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 14:08:55 2025

@author: Luerig
"""

import gymnasium as gym
import simpy
import Framework.ScriptGenerator as Movie
import numpy as np

from Framework.Simulation import WaitingModule

class CashierSimulator:
    
    MaxFillingCashLines = 10
    # All the following values are gamma distributed with mean and std deviation gicen
    TimeBetweenCustomers = (2.0, 1.0)
    TravelTime = (2.0, 1.0)
    WorkingSlow = (7.0, 2.0)
    WorkingFast = (4.0, 1.0)
    LeavingTime = (3.0, 0.5)
    
    MaxTime = 300
    FailureReward = -1.0
    CustomerReward = 0.01
    
    
    '''Contains the transfer times from yource to destination station'''
    
    def __init__(self, generatesMovie, usesAutoDispatcher):
        '''
        

        Parameters
        ----------
        generatesMovie :  
            bool if we want to generate a movie

        usesAutoDispatcher:
            In the case of auto dispatcher the dispatcher  does cyclic dispatching of customers.
        Returns
        -------
        None.

        '''
        self.__generatesMovie = generatesMovie
        self.__usesAutoDispatcher = usesAutoDispatcher

      
    
    @property
    def ActionArray(self):
        '''
            The amount of actors the environment support. Every action for every worker.
            We have the cahsier slow and fast. Both can process a customer or walk to cashier 0,1,2
            We have a the dispatcher that can dispatch to line 0,1,2

        Returns
        -------
        list
            Number of acions that every worker can perform.

        '''
       
        return  [4,4] if self.__usesAutoDispatcher else [4,4,3]
    
    
    @property
    def Terminated(self):
        '''
        Indicates, if the environment is terminated (meaning episode s over.)

        Returns
        -------
         
            True if over here we either have the time managed or a que is overrun.

        '''
        return self.__env.now > CashierSimulator.MaxTime or self.__queOverrun
    
    @property
    def TimeOut(self):
        '''
        Gives the time out used for deadlock detection.
        Should rarely happen in this scenario.

        Returns
        -------
        float
            Float time for deadlock detection.

        '''
        return 100.0
    
    @property
    def TimeOutPenalty(self):
        '''
        Gives the reward for the case that we run in a timeout and therefore probably a deadlock.
        Should be calibrated in relation to the rest of the reward.

        Returns
        -------
         
            penalty for dedalock.

        '''
        return -10.0
    
    @property 
    def MovieScript(self):
        '''
        Gets the movie script used to generate a movie.

        Returns
        -------
         
            The movie script.

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
        return {'Line A': gym.spaces.Discrete(CashierSimulator.MaxFillingCashLines + 1),
                'Line B': gym.spaces.Discrete(CashierSimulator.MaxFillingCashLines + 1),
                'Line C': gym.spaces.Discrete(CashierSimulator.MaxFillingCashLines + 1),
                # 3: Beeing at cash 1,2,3 :  3 Transition to cash 1,2,3
                'Slow' : gym.spaces.Discrete(6),
                'Fast' : gym.spaces.Discrete(6),
                'Time' : gym.spaces.Box(0.0, 1.0, shape=(1,), dtype =np.float32)
                }
    
    
    def GetObservation(self):
        '''
        Function that generates the current observation.

        Returns
        -------
        dict
            Observation dictionary.

        '''
        
        return {'Line A': self.__customerQue[0].level,
                'Line B': self.__customerQue[1].level,
                'Line C': self.__customerQue[2].level,
                # 3: Beeing at cash 1,2,3 : Transition to cash 1,2,3
                'Slow' : self.__cashierAtOrGoingToStation[0] +
                        (3 if self.__cashierCurrentlyInTransfer[0] else 0),
                'Fast' : self.__cashierAtOrGoingToStation[1] +
                        (3 if self.__cashierCurrentlyInTransfer[1] else 0),        
                        
                            
                'Time' :  [np.clip(self.__env.now / CashierSimulator.MaxTime, 0.0, 1.0)]
                }
    
    
    
    
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
        self.__accumulatedCustomers = 0
        self.__customerIndexCounter = 0
        
        # Used in the case of auto dispatcher.
        self.__lastDispatched = 2
        
        self.__waiting = WaitingModule.WaitingModule(simPyEnv, randGen)
        '''The module that can do random waiting'''
        
        
        if self.__generatesMovie:
            self.__movie = Movie.ScriptGenerator(simpyEnv = simPyEnv)
            # First the ques.
            self.__movie.AddAction('Que0', 0)
            self.__movie.AddAction('Que1', 0)
            self.__movie.AddAction('Que2', 0)
            
            # The actions of the different cashiers.
            self.__movie.AddAction('CashSlow', {'State' : 'Working', 'Station' : 0})
            self.__movie.AddAction('CashFast', {'State' : 'Working', 'Station' : 1})
            
            
            # Customers served.
            self.__movie.AddAction( 'Custs', 0)
            self.__movie.AddAction( 'Time', None)
        
        
        
        self.__cashierCurrentlyInTransfer = [False, False]
        '''Flags if the cashier is currently moving'''
        self.__cashierAtOrGoingToStation = [0, 1]
        '''Flags where cahsier currently is or is going to.'''
        self.__customerQue = [simpy.Container(simPyEnv, capacity = CashierSimulator.MaxFillingCashLines),
                              simpy.Container(simPyEnv, capacity = CashierSimulator.MaxFillingCashLines),
                              simpy.Container(simPyEnv, capacity = CashierSimulator.MaxFillingCashLines)
                             ] 
        
        
        
        '''The container used for the customer arrival process.'''
        '''Contains the filling of the customers ques.'''
        self.__stationOccupied = [True, True, False]
        '''Contains the information if the station is currently overruned'''
        self.__queOverrun = False
        '''Flags if any of the three quees is overrrun'''
        
        if self.__usesAutoDispatcher:
            self.__env.process(self.__runAutoDispatcher())
        

       
        
       
      
    
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
        
        # The dispatcher has nothing to do.
        if actorChosen == 2:
           return
        
        # The casheris have to pay attention when they relocate. 
        if localAction != 0:
            source = self.__cashierAtOrGoingToStation[actorChosen]
            destination = localAction - 1
            self.__stationOccupied[source] = False
            self.__stationOccupied[destination] = True
        
    
  
    def __runAutoDispatcher(self):
        '''
        Helper routine to run an automatic dispatcher.

        Yields
        ------
            Waiting event for dispatching.

        '''
        while True:
            self.__lastDispatched = (self.__lastDispatched + 1) % 3
            yield from self.__handleDispatcher(self.__lastDispatched)
            
        
    def __handleDispatcher(self, localAction):
        '''
        Handles the disptacher action.

        Parameters
        ----------
        localAction : 
            The action we like to do.

        Yields
        -------
            Waiting events for the simulation.


        '''
        
      
        # Where dis the last dipatch happen?
        if self.__generatesMovie:
            self.__movie.AddAction('LastDispatch', localAction)
        
            
        yield self.__waiting.WaitGamma(CashierSimulator.TimeBetweenCustomers)
        
        
        # Check if our destination que is full and we fail.
        if self.__customerQue[localAction].level == CashierSimulator.MaxFillingCashLines:
            self.__queOverrun = True
            self.__reward += CashierSimulator.FailureReward
            if self.__generatesMovie:
                self.__movie.AddAction('QueBusted', localAction)
            return
        
        # Now we can disptach the customer.
        yield self.__customerQue[localAction].put(1)
        
        # Arrival is finished.
        if self.__generatesMovie:
            self.__movie.AddAction(f"Que{localAction}", self.__customerQue[localAction].level)
            
        
    
        
    def __TerminateLeavingCustomer(self, custActor):
        '''
        Simple function that terminates a certain action after a certain time.

        Parameters
        ----------
        custActor : 
            The action we want to terminate.

        Yields
        ------
            Waiting event.

        '''
        
        yield self.__waiting.WaitGamma(CashierSimulator.LeavingTime)
        self.__accumulatedCustomers += 1
        if self.__generatesMovie:
            self.__movie.AddAction( 'Custs', self.__accumulatedCustomers)
            self.__movie.CloseAction(custActor)
        
        
    def __handleCashier(self, isSlowCashier, localAction):
        '''
        Handles the cashier.

        Parameters
        ----------
        isSlowCashier :
            Indicates the slow cashier.
        localAction : TYPE
            The action we do 0: process customer, 1-3: go to other station.

        Yields
        -------
            Waiting events for the simulation.

        '''
        
        actor = 'CashSlow' if isSlowCashier else 'CashFast'
        localIndex = 0 if isSlowCashier else 1
        currentStation = self.__cashierAtOrGoingToStation[localIndex]
        self.__cashierCurrentlyInTransfer[localIndex] =  False
        if localAction == 0:
            # In this case we are working.
            if self.__generatesMovie:
                self.__movie.AddAction(actor, {'State' : 'Stalled', 'Station' : currentStation})
            
            # Get one customer.
            yield self.__customerQue[currentStation].get(1)
            
            if self.__generatesMovie:
                self.__movie.AddAction(actor, {'State' : 'Working', 'Station' : currentStation})
                self.__movie.AddAction(f"Que{currentStation}", self.__customerQue[currentStation].level)
                
           
            yield self.__waiting.WaitGamma(CashierSimulator.WorkingSlow if isSlowCashier else 
                                     CashierSimulator.WorkingFast)
           
            if self.__generatesMovie:
                self.__movie.AddAction(actor, {'State' : 'Stalled', 'Station' : currentStation})
           
            # Get a small reward for  the customer.
            self.__reward += CashierSimulator.CustomerReward
            self.__customerIndexCounter += 1
            
            custActor = f"LeavingCust{self.__customerIndexCounter}"
            # Here we spawn a leaving customer.
            if self.__generatesMovie:
                self.__movie.AddAction(custActor, currentStation)
            
            self.__env.process(self.__TerminateLeavingCustomer(custActor))
        else:
            # In this case we want to transfer to a station.
            destination = localAction - 1
            
            
            self.__cashierCurrentlyInTransfer[localIndex] = True
            
            self.__cashierAtOrGoingToStation[localIndex] = destination
            if self.__generatesMovie:
                self.__movie.AddAction( actor, 
                                      {'State': 'Walking' , 
                                       'Station' : currentStation,
                                       'Destination' : destination})
                
            yield self.__waiting.WaitGamma(CashierSimulator.TravelTime)
            
            
    
    def PerformAction(self, actorChosen, localAction):
        '''
        Performs an action of the chosen actor with the indicated index of the action of that specific actor.

        Parameters
        ----------
        actorChosen :  
            The actor that performs the action.
        localAction :  
            The action done on that actor.

        Yields
        -------
            Waiting events from the simulation.

        '''
      
      
        if actorChosen == 2:
            yield from self.__handleDispatcher(localAction)
        else:
            yield from self.__handleCashier((actorChosen == 0), localAction)
      
            
    
    
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


        # The dispatcher can always pick any element.
        if (actorChosen == 2):
            return [True, True, True]
        
        # The cahier can always work but we can not go to a station that is currently occupied.       
        result = [True] + [not x for x in self.__stationOccupied]
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
    
        
   
        
      
        
   
     