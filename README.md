# SimReinforce
This is a framework for integrating Simpy, StableBaselines, and GamePy for Multi-Actor Situations.


## Example 
As an example, I have added a factory simulation.

https://github.com/user-attachments/assets/0347a139-d725-4e17-ae06-412c79cfa64d

The factory has three processing stages. The second stage has two working places, the first and the third one. 
Processing stages are coupled via buffers with 10 places each. Working on stage 1 and 3 takes 5 seconds, on stage 2, 10
seconds. Workers may change working places, going from stage 1 to 2 and from 2 to 3 takes 4 seconds from stage 1 to 3 8 seconds. 
Theoretically, workers can also change between the two working places at stage 2, which would take 1 second. The objective is now for the RL Agent to get
as many items manufactured in 5 minutes as possible. The video is in fast-forward mode by a factor of 5. If you train your model yourself, it might take a couple of
experiments to get to 28 items manufactured. 27 can be reached pretty reliably.

## Used python modules
- gymnasium
- stable_baselines3
- sb3_contrib
- simpy
- numpy
- gamepy
- moviepy

# General Strategy


