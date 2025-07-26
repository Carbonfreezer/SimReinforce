# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 15:19:33 2025

@author: Luerig
"""


import pickle as pk
class ScriptGenerator:
    
    def __init__(self, simpyEnv = None):
        self.__env = simpyEnv
        '''The simpy environment to ask for the current time'''
        self.__logList = []
        '''The list with all the log entries from the script'''
        self.__openEntries = {}
        '''The dictionary that contains the association between actor and the opened entry'''

    
    @staticmethod    
    def __makeLogEntry(startTime, actor, stateInformation):
        return {'Start' : startTime, 'Actor' : actor, 'Info' : stateInformation}
    
    def AddAction(self,  actor, stateInformation):
        '''
        Adds a new action to the log entry

        Parameters
        ----------
        actor : TYPE
            The actor who does it.
        stateInformation : TYPE
            Information concerning the state of the actor.

        Returns
        -------
        None.

        '''
        
        currentTime = self.__env.now
        if actor in self.__openEntries:
            self.__openEntries[actor]['End'] = currentTime
            
        newLog = self.__makeLogEntry(currentTime, actor, stateInformation)
        self.__logList.append(newLog)
        self.__openEntries[actor] = newLog
        
        
    def CloseAllEntriesAndGetLogList(self):
        '''
        Closes all entries from all actors. Usually done at the end of the simuation.
        Returns the loglist.

     
        Returns
        -------
        TYPE
            The loglist.


        '''
        for entry in self.__openEntries.values():
            entry['End'] =  self.__env.now
        self.__openEntries = {}
        return self.__logList
        

    @staticmethod
    def LoadScript( fileName):
        '''
        Loads a script from a filename.

        Parameters
        ----------
        fileName : TYPE
            File to load.

     

        '''
        handle = open(fileName, 'rb')
        script = ScriptGenerator()
        script.__logList =  pk.load(handle)
        return script
    
    def GetAllInterpolatedEntries(self, time):
        '''
        Asks the script for a specific log for a time in the script.

        Parameters
        ----------
        time : TYPE
            DESCRIPTION.

        Returns
        -------
        result : TYPE
            The status information of all relevant actors.

        '''
        filteredEntries = (x for x in self.__logList if x['Start'] <= time and x['End'] > time)
        result = {}
        for entry in filteredEntries:
            interPolValue = (time - entry['Start']) / (entry['End'] - entry['Start'])
            assert not entry['Actor'] in result, "Double Actor information"
            result[entry['Actor']] =  {'Factor' : interPolValue, 
                                       'Info' : entry['Info']}
            
        return result
    
    @property
    def MaxTime(self):
        '''
        Asks for the maximum (exclusive time) of the script.

        Returns
        -------
        TYPE
            The complete time of the script.

        '''
        return max((x['End'] for x in self.__logList))
        