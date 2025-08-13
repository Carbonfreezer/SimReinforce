# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 09:37:40 2025

@author: Luerig
"""

import numpy as np
import pygame as pg

def PaintSprite(destination, source, point):
    '''
    Helper method to paint a sprite centered at the indicated point (coordinates)

    Parameters
    ----------
    destination :  
        Destination surface where to draw to.
    source :  
        Image (surface) to draw.
    point :  
        Numpy array of point to draw.

    Returns
    -------
    None.

    '''
    rect = source.get_rect()
    targetPoint = point - [rect.width * 0.5, rect.height * 0.5]
    destination.blit(source, targetPoint)
    
    
    
    
def GetColorizedSprite(source, color):
    '''
    Gets a colorized (multiplied) version of a white transparent sprite.

    Parameters
    ----------
    source :
        The sprite we want to colorize
    color : 
        The color we want to multiply the sprite with.

    Returns
    -------
    proxy : 
        The colorized sprite.

    '''
    
    proxy = pg.Surface(source.get_size())
    proxy.fill(color)
    proxy.blit(source, (0, 0), special_flags=pg.BLEND_MULT)
    return proxy


def GetHDBackground(color="Black"):
    '''
    Returns an image with default HD resolution and identified color.

    Parameters
    ----------
    color :  optional
        The background color of the background image. The default is "Black".

    Returns
    -------
    surface : 
        Background sprite.

    '''    
    surface = pg.Surface(1920, 1080)
    surface.fill(color)
    return surface


def PrintText(surface, text, font, position, color = "White"):
    '''
    Prints a text with an indicated font at a specific position.

    Parameters
    ----------
    surface : 
        The destination surface where to print the text to.
    text : 
        The text we want to write.
    font : 
        The font we write with.
    position : TYPE
        Central position to write to.
    color : optional
        Printing color. The default is "White".

    Returns
    -------
    None.

    '''
    
    img = font.render(text, True, color)
    PaintSprite(surface, img, position)
    
 
    

def PaintSpritePointing(destination, source, drawingPoint, orientationPoint):
    '''
    Draws a orientated sprite like an arrow. The sprite is painted  centered at the drawing
    point and its horrizontal axis is orientation to the orientattionPoint

    Parameters
    ----------
    destination :
        Destination surface to blit to.
    source : 
        Source surface that is painted.
    drawingPoint : TYPE
        The point where we draw to.
    orientationPoint : TYPE
        The point we orientate the right direction of the sprite to.

    Returns
    -------
    None.

    '''
    
    delta = orientationPoint - drawingPoint
    angle = np.arctan2(delta[1], delta[0])
    angle = - np.rad2deg(angle)
    
    finalImage = pg.transform.rotate(source, angle)
    rect = finalImage.get_rect()
    targetPoint = drawingPoint - [rect.width * 0.5, rect.height * 0.5]
    destination.blit(finalImage, targetPoint)
    