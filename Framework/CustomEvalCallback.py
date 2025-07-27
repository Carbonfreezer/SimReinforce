# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 09:22:02 2025

@author: Luerig
"""


class CustomEvalCallback:
    '''This is a simple helper class to generate a snapshot with a certain filename'''
    def __init__(self, fileName):
        '''
        Stores the fielname we want to save the model to on successfull checkpoint.

        Parameters
        ----------
        fileName : TYPE
            The file we want to save the model to.

        Returns
        -------
        None.

        '''
        self.__fileName = fileName
        
    def init_callback(self, model):
        self.__model = model
        
    def on_step(self) -> bool:
        print(f"Generating file {self.__fileName}")
        self.__model.save(self.__fileName)        
        return True
    
    