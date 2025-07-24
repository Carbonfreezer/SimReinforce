# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 16:45:24 2025

@author: Luerig
"""

from sb3_contrib import MaskablePPO


import FactoryPlugin
import Framework.FrameworkGym as Frame
from sb3_contrib.common.maskable.utils import get_action_masks

env = Frame.FrameworkGym(generator = FactoryPlugin.FactoryPlugin, generateMovieScript=True)
model = MaskablePPO.load("best_model", print_system_info=True, env=env)

env = model.get_env()
obs = env.reset()
terminated = False
while not terminated:
    action_masks = get_action_masks(env)
    action, _state = model.predict(obs, deterministic=True, action_masks=action_masks)
    obs, reward, terminated, info = env.step(action)
 

   
info[0]['Script'].SaveScript("Skript.pkl")        
  