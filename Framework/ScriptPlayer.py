# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 09:15:10 2025

@author: Luerig
"""

class ScriptPlayer:
    def __init__(self, logList):
        '''
        Creates the scipt player from the indicated loglist.

        Parameters
        ----------
        logList : 
            log list to create player from.

        Returns
        -------
        None.

        '''
        self.__logList = logList
        
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
            
       