# SimReinforce
This is a framework for integrating Simpy, StableBaselines, and GamePy for Multi-Actor Situations.


## Example 
As an example, I have added a factory simulation.

https://github.com/user-attachments/assets/0347a139-d725-4e17-ae06-412c79cfa64d

The factory has three processing stages. The second stage has two working places, the first and the third one. 
Processing stages are coupled via buffers with 10 places each. Working on stages 1 and 3 takes 5 seconds, and on stage 2, it takes 10 seconds. 
Workers may change their working places, and the transition from stage 1 to 2 and from 2 to 3 takes 4 seconds, while the transition from stage 1 to 3 takes 8 seconds. 
Theoretically, workers can also change between the two working places at stage 2, which would take 1 second. The objective is now for the RL Agent to get
as many items manufactured in 5 minutes as possible. The video is playing at 5 times the normal speed. If you train your model yourself, it might take a couple of
experiments to get to 28 items manufactured. 27 can be reached pretty reliably.

## Used python modules
- gymnasium
- stable_baselines3
- sb3_contrib
- simpy
- numpy
- gamepy
- moviepy

## General Strategy
The objective is to have a gym with multiple actors that are controlled via Maskable PPO from stable baselines that is running on a simpy environment. 
Simpy is a discreet event simulator. As a next step, we want to create a continuous video from it, as shown in the example above.

The first problem is that OpenAI Gym only supports a single actor. We solve this by adding the actor index for which we want a decision to the observation space. 
The action space we use is discrete and contains all possible actions for all actors. When an action of a specific actor is required all other action options are masked out over the maskable 
PPO algorithm. The specific decisions are then started as a simpy process. As several actors may wait for a new command simultaneously, we maintain a list of actors who are waiting for a command. 
Once there are no more waiting actors, the simpy environment is run until at least one actor is finished. To prevent deadlocks, we also combine this with a timeout event to detect possible deadlock situations.
This core concept is reflected in the **step** function of **FrameworkGym**.

As a next step, we want to generate a Video from the simulation. The OpenAI gym already provides this option. Unfortunately, this generates a movie frame after every step call. As we have coupled the Gym with a discrete event simulator in simpy
The time passed in different calls of the step function may vary significantly. Also, for certain aspects like moving objects, we want to provide an interpolated transition between states. The way we solved this problem is to generate a log during a trial run, 
which logs which object caused which event and when. This log is administered in the class **ScriptGenerator** of the framework. 


