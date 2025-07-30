# SimReinforce
This framework integrates Simpy, StableBaselines, and GamePy to render a time-continuous movie using MoviePy for multi-actor situations.


## Examples

### Factory Example 
The demonstration features a three-stage manufacturing process where an RL agent optimizes worker allocation to maximize production within a 5-minute timeframe:

https://github.com/user-attachments/assets/0347a139-d725-4e17-ae06-412c79cfa64d

#### System Architecture:
- Stage 1 & 3: Single workstation each (5-second processing time)
- Stage 2: Dual workstations (10-second processing time)
- Buffer capacity: 10 items between each stage
#### Worker mobility: Dynamic reallocation between stages 
- Stage 1↔2 or Stage 2↔3: 4 seconds
- Stage 1↔3: 8 seconds
- Within Stage 2 workstations: 1 second

#### Objective: 
Train the RL agent to optimize worker positioning and workflow to achieve maximum throughput in the given time constraint.

#### Observations
The generated visualization runs at 5x speed to efficiently demonstrate the learning process and system dynamics.
If you train your model yourself, you should reach 28 items manufactured.


### Cashier Example
This example demonstrates a chashier situation. This example is stochastic. All used working times use a 
gamma distribution specified by the mean and standard deviation. The example contains two cashiers and a dispatcher.
The AI can control the dispatcher and cashier:


https://github.com/user-attachments/assets/56112eb2-cc45-4546-810a-04e846797874


Or it can be in automatic mode, where it dispatches customers in cycles to the dispatching lines, and only cashiers are controlled by the AI:


https://github.com/user-attachments/assets/57050cf7-7fbe-4e9d-8430-057944b6f3f4


### System architecture
- First, a dispatcher dispatches the customers to one of the three lanes - time: (mean: 2.0, stddev: 1.0)
- Then there are waiting queues for the three lines with 10 positions.
- A slow cashier processing time   (mean: 7.0, stddev: 2.0)
- A fast cashier processing time   (mean: 4.0, stddev: 1.0)
- All cashiers can transfer between positions (mean: 2.0, stddev: 1.0)

#### Objective
Run the system for 5 minutes without a lane running over 10 customers.


#### Observations
Due to the stochastic nature, success is not guaranteed. When the AI controls the dispatcher,
the cashiers are not moving around, and the dispatcher solely does load balancing. When the dispatcher is in auto
mode, mainly the fast cashier tries to service two lines. 

The obtained mean reward for intelligent mode, where the AI controls the dispatcher, was 0.33, and for the 
auto mode -0.23.  


## Used python modules
- gymnasium
- stable_baselines3
- sb3_contrib
- simpy
- numpy
- gamepy
- moviepy

## General Strategy
The objective is to create a gym with multiple actors controlled via Maskable PPO from stable baselines, running in a Simpy environment. 
Simpy is a discreet event simulator. As a next step, we want to create a continuous video from it, as shown in the example above.

The first problem is that OpenAI Gym only supports a single actor. We solve this by adding the actor index for which we want a decision to the observation space. 
The action space we use is discrete and contains all possible actions for all actors. When an action of a specific actor is required, all other action options are masked out over the maskable 
PPO algorithm. The specific decisions are then started as a simpy process. As several actors may wait for a new command simultaneously, we maintain a list of actors who are waiting for a command. 
Once there are no more waiting actors, the simpy environment is run until at least one actor is finished. To prevent deadlocks, we also combine this with a timeout event to detect possible deadlock situations.
This core concept is reflected in the **step** function of **FrameworkGym**.

As a next step, we want to generate a Video from the simulation. The OpenAI gym already provides this option. Unfortunately, this generates a movie frame after every step call. As we have coupled the Gym with a discrete event simulator in simpy
The time passed in different calls of the step function may vary significantly. Additionally, for certain aspects, such as moving objects, we want to provide an interpolated transition between states. The way we solved this problem is to generate a log during a trial run, 
which logs which object caused which event and when. This log is administered in the class **ScriptRecorder** of the framework. Whenever an actor makes a new decision, the old one is flagged as finished, and a new one begins. This way, continuous transitions can be displayed in
the visualization. This could be done, for instance, if the event involves walking from A to B. The framework's user must implement this logging and is not limited to actors controlled by the AI. The class **ScriptPlayer** is used later on in the movie system to play back the script.

If a script is provided, world situations can be generated for specific points in time. The **MovieMaker** class extracts this information and calls a render plugin to create an image based on the given information. As the framework will most likely be used
for situations where things move around and objects get stored, several helper classes are provided for these tasks. First, there are two types of bar visualizations (**ContinuousBar** and **DiscreteBar**), and second, there is a helper class (**PositionManager**) that helps with painting
sprites at specific positions on the screen. Positions can be handed over with names and paths, as a connection of points can be specified. Paths are a means to help with positional animation. Given a completion percentage, a position can be extracted along the path.

The main functions are in **GlobalFunctions**. There are two functions: one to train the MaskabePPO learner (**PerformTraining**) and another to execute an episode, log it, and generate a video (**GenerateMovie**).

## Getting Started
The best way to get started is to look at the Python files in the subfolders of the **Example** folder. The file **TestFunctions** serves as the main entry point. The **FSimulator** file is the plugin for the OpenGym environment, responsible for the simulation. The file **Painter** is the plugin that is responsible for rendering a specific situation. If you want to program your application, create a new subfolder and implement these classes as well. Take a look at the public properties and methods. You also need to implement them. The link between the simulation and the rendering is the log
 for the script generator. The best approach is to consider the changes in your simulation. These things become specific to a particular actor and are defined in the reset function of your plugin. Whenever these objects change, you can log the required information with the **AddAction** command. How these objects get visualized later on is handled in the painter module. 

If you are used to OpenAI gyms, what may be a bit confusing here is that the system controls several actors. What corresponds to the step function is the combination of **PrepareAction** and **PerformAction**. These functions are actor-specific. PerformAction is the actual process. Several processes may run concurrently. To prevent collisions between actions, such as two persons walking to the same position, you must implement this in the PrepareAction method. Also, as several things may happen at the same time, the reward for several actions may be accumulated, as you can also see in the example. They get retrieved and reset by the **GetAndResetReward** function.
Action masking is also done actor-specific by the **actions_masks** function.


