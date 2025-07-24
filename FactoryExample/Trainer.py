# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 11:47:46 2025

@author: Luerig
"""


import gymnasium as gym
import os
from sb3_contrib import MaskablePPO
from sb3_contrib.common.maskable.callbacks import MaskableEvalCallback

import FactoryPlugin
import Framework.FrameworkGym as Frame
import torch as th



# env = PortfolioEnv()
# env = ActionMasker(env,action_mask_fn=PortfolioEnv.action_masks)
# env = DummyVecEnv([lambda: env])

env = Frame.FrameworkGym(generator = FactoryPlugin.FactoryPlugin)
# env = gym.make("gymnasium/Processing", generator = FactoryPlugin.FactoryPlugin)

policy_kwargs = dict(activation_fn=th.nn.ReLU,
                     net_arch=dict(pi=[64,64], vf=[64, 64]))

model = MaskablePPO("MultiInputPolicy", env, verbose=0) #  policy_kwargs=policy_kwargs)



# Create log dir where evaluation results will be saved
eval_log_dir = "./eval_logs/"
os.makedirs(eval_log_dir, exist_ok=True)

eval_callback = MaskableEvalCallback(env, best_model_save_path=eval_log_dir,
                              log_path=eval_log_dir, eval_freq=100_000,
                              n_eval_episodes=100)



model.learn(total_timesteps=500_000, callback=eval_callback)
