# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 15:19:33 2025

@author: Luerig
"""


import pickle as pk
class ScriptGenerator:
    
    def __init__(self):
        self.__logList = []
        '''The list with all the log entries from the script'''
        self.__openEntries = {}
        '''The dictionary that contains the association between actor and the opened entry'''
        
    
    @staticmethod    
    def __makeLogEntry(startTime, actor, stateInformation):
        return {'Start' : startTime, 'Actor' : actor, 'Info' : stateInformation}
    
    def AddAction(self, currentTime, actor, stateInformation):
        '''
        Adds a new action to the log entry

        Parameters
        ----------
        currentTime : TYPE
            The time when the change occured.
        actor : TYPE
            The actor who does it.
        stateInformation : TYPE
            Information concerning the state of the actor.

        Returns
        -------
        None.

        '''
        if actor in self.__openEntries:
            self.__openEntries[actor]['End'] = currentTime
            
        newLog = self.__makeLogEntry(currentTime, actor, stateInformation)
        self.__logList.append(newLog)
        self.__openEntries[actor] = newLog
        
    def CloseActor(self, actor, currentTime):
        '''
        Closes the active entryy from a specific actor.

        Parameters
        ----------
        actor : TYPE
            The actor we want to remove information from.
        currentTime : TYPE
            The time whent he change occured.

        Returns
        -------
        None.

        '''
        assert actor in self.__openEntries, "Actor is not in open entries"
        self.__openEntries[actor]['End'] = currentTime
        del self.__openEntries[actor]
        
    def CloseAllEntries(self, currentTime):
        '''
        Closes all entries from all actors. Usually done at the end of the simuation.

        Parameters
        ----------
        currentTime : TYPE
            The time when the actos got closed.

        Returns
        -------
        None.

        '''
        for entry in self.__openEntries.values():
            entry['End'] = currentTime
        self.__openEntries = {}
        
    def SaveScript(self, fileName):
        '''
        Saves the script to a file.

        Parameters
        ----------
        fileName : TYPE
            The name of the file to load from

        Returns
        -------
        None.

        '''
            
        file = open(fileName, 'wb') 
        pk.dump(self, file)
        
    @staticmethod
    def LoadScript(fileName):
        '''
        Loads a script from a filename.

        Parameters
        ----------
        fileName : TYPE
            File to load.

        Returns
        -------
        TYPE
            The loaded file

        '''
        handle = open(fileName, 'rb')
        return pk.load(handle)
    
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
        