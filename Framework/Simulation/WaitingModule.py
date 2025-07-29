# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 14:20:46 2025

@author: Luerig
"""


class WaitingModule:
    def __init__(self, simpyEnv, random):
        '''
        Initializes the waiting module to generate random waiting events.

        Parameters
        ----------
        simpyEnv : 
            The simpy environment we use.
        random : 
            Random number generator provided by the gym

        Returns
        -------
        None.

        '''
        self.__simpyEnv = simpyEnv
        self.__random = random
        
        
        
    def WaitExponential(self, mean):
        '''
        Generates an event for waiting with an exponential distribution. 
        These are usually used for outside events, where there is a certain probability
        that an event happens within a certain time interval. Those events are not coupled.

        Parameters
        ----------
        mean : TYPE
            The mean time, that passes between events happening.

        Returns
        ------
            The simpy time event-

        '''
        return self.__simpyEnv.timeout(self.__random.exponential(scale=mean))
        
    def WaitGamma(self,inVal):
        '''
        Creates a time out event according to a gamma distribution. Gamma distributions
        are usually used for working times on a certain task. 

        Parameters
        ----------
        inVal : 
            Inval is a tuple of mean and standard deviation of the used gamma distribution.

        Returns
        -------
            The timeout event for the given parameters.

        '''
        
        mean, std = inVal
        scale = (std ** 2) / mean
        shape = mean / scale
        
        return self.__simpyEnv.timeout(self.__random.gamma(shape, scale))
        
        