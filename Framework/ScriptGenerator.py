# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 15:19:33 2025

@author: Luerig
"""

import copy

class ScriptGenerator:
    
    def __init__(self, simpyEnv = None, logList = None):
        '''
        Initializes the script generator.

        Parameters
        ----------
        simpyEnv :  , optional
            The simpy environment. This is a must when generating the log in simulation. The default is None.
        logList :  , optional
            This is the list with the log entries. This entry is only used when the video gets generated. The default is [].

        Returns
        -------
        None.

        '''
        self.__env = simpyEnv
        '''The simpy environment to ask for the current time'''
        if logList == None:
            self.__logList = []
        else:
            self.__logList = logList
        '''The list with all the log entries from the script'''
        
        self.__openEntries = {}
        '''The dictionary that contains the association between actor and the opened entry'''
        

    
    
    def AddAction(self,  actor, stateInformation):
        '''
        Adds a new action to the log entry

        Parameters
        ----------
        actor :  
            The actor who does it.
        stateInformation :  
            Information concerning the state of the actor.
            This may be some arbitrary information.

        Returns
        -------
        None.

        '''
        
        currentTime = self.__env.now
        
        if actor in self.__openEntries:
            self.__openEntries[actor]['End'] = currentTime
            
        newLog = {'Start' : currentTime, 'Actor' : actor, 'Info' : stateInformation}
        self.__logList.append(newLog)
        self.__openEntries[actor] = newLog
        
        
    def CloseAction(self, actor):
        '''
        Closes an action.

        Parameters
        ----------
        actor : 
            The actor whose current action should terminate.

        Returns
        -------
        None.

        '''
        self.__openEntries[actor]['End'] = self.__env.now
        del self.__openEntries[actor]
        
        
    def CloseAllEntriesAndGetLogList(self):
        '''
        Closes all entries from all actors. Usually done at the end of the simuation.
        Returns the loglist.

     
        Returns
        -------
         
            The loglist.


        '''
        
        for entry in self.__openEntries.values():
            entry['End'] =  self.__env.now
        
        self.__openEntries = {}
        return  copy.deepcopy( self.__logList)
        

    
    def GetAllInterpolatedEntries(self, time):
        '''
        Asks the script for a specific log for a time in the script.

        Parameters
        ----------
        time :  
            The time where to extract the data for.

        Returns
        -------
        result :  
          The result set is a dictionary associating the name of an actor with another dictionary.
          This dictionary has the entries 'Progress' which is s float between [0,1] 
          and can be used to map the situation to a continuous change, and an entry 'Info' which is arbitrary data
          from the logging system.

        '''
        filteredEntries = (x for x in self.__logList if x['Start'] <= time and x['End'] > time)
        result = {}
        for entry in filteredEntries:
            interPolValue = (time - entry['Start']) / (entry['End'] - entry['Start'])
            assert not entry['Actor'] in result, "Double Actor information"
            result[entry['Actor']] =  {'Progress' : interPolValue, 
                                       'Info' : entry['Info']}
            
        return result
    
    
    def GetLastState(self):
        '''
        Gets the last state of the log. Needed for closing a movie.
        Result is the same as for GetAllInterpolatedEntries.

        Returns
        -------
        result :  
            The result set is a dictionary associating the name of an actor with another dictionary.
            This dictionary has the entries 'Progress' which is s float between [0,1] 
            and can be used to map the situation to a continuous change, and an entry 'Info' which is arbitrary data
            from the logging system.

        '''
        endTime = self.MaxTime
        filteredEntries = (x for x in self.__logList if x['End'] == endTime)
        result = {}
        for entry in filteredEntries:
            result[entry['Actor']] =  {'Progress' : 1.0, 
                                       'Info' : entry['Info']}
            
        return result
        
    
    
    
    
    @property
    def MaxTime(self):
        '''
        Asks for the maximum time of the script.

        Returns
        -------
         
            The complete time of the script.

        '''
        return max((x['End'] for x in self.__logList))
        