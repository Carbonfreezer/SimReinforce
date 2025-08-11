# -*- coding: utf-8 -*-
"""
Created on Sat Aug  9 14:05:31 2025

@author: chris
"""


class EmergencyCallCategory:
    
    def __init__(self, priority, averageTime, rewardMax, rewardMin, timeMin, timeMax, 
                 neededResources, neededTime):
        '''
        Creates one of the categories of 

        Parameters
        ----------
        priority : 
            Priority level of the ermergency call.
        averageTime:
            The average time that passes between two emergency calls.
        rewardMax : 
            Maximum reward we get.
        rewardMin : 
            Minimal reward we get for completion in the end.
        timeMin : 
            Time, when the reward starts declining.
        timeMax : 
            The time, when the minimal reward is reached.
        neededResources :
            Array of ressources used by the emergency call. 
        neeededTime:
            Time for executing the emergeny call by the ambulance. Given by mean time and standard deviation.

        Returns
        -------
        None.

        '''
        
        self.__priority = priority
        self.__averageTimeBetween = averageTime
        self.__rewardBracket = (rewardMax, rewardMin)
        self.__timeBracket = (timeMin, timeMax)
        self.__neededResources = neededResources
        self.__neededTime = neededTime
    
    @property
    def Priority(self):
        return self.__priority
    
    @property
    def AverageTimeBetweenCalls(self):
        return self.__averageTimeBetween
    
    @property
    def NeededTime(self):
        return self.__neededTime
    
    @property
    def NeededResources(self):
        return self.__neededResources
    
    def GetReward(self, neededTime):
        if neededTime < self.__timeBracket[0]:
            return self.__rewardBracket[0]
        elif neededTime > self.__timeBracket[1]:
            return self.__rewardBracket[1]
        
        return self.__rewardBracket[1] + (self.__rewardBracket[0] - self.__rewardBracket[1]) * \
                (neededTime - self.__timeBracket[0]) / (self.__timeBracket[1] - self.__timeBracket[0])