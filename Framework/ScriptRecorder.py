# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 15:19:33 2025

@author: Luerig
"""

class ScriptRecorder:
    
    def __init__(self, simpyEnv , wantsMovie):
        '''
        Initializes the script recorder if we want to generate a script.

        Parameters
        ----------
        simpyEnv :
            The simpy environment. 
        wantsMovie:
            bool Flag if we want to generate a movie
        
        Returns
        -------
        None.

        '''
        self.__env = simpyEnv
        '''The simpy environment to ask for the current time'''
        self.__wantsMovie = wantsMovie
        
        self.__logList = []
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
        
        if not self.__wantsMovie:
            return
        
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
        
        if not self.__wantsMovie:
            return
        
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
        
        if not self.__wantsMovie:
            return []
        
        for entry in self.__openEntries.values():
            entry['End'] =  self.__env.now
        
        self.__openEntries = {}
        return  self.__logList
        

    
   