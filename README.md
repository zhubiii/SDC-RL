# SDC-RL
Testing Reinforcement Learning for Self-Driving Cars in Urban Environments using Pygame

Used Deep-Q network model to train our agent. See [Creating Maps](#creating-maps) to learn how to make custom maps. 

## Usage
- main.ipynb is primarily for human teleoperation and fun
- sdcDQL.ipynb is to run the Deep-Q RL model
    - The code should be well documented
- trained models are saved in to the models folder
- On launch a window showing the detected lines as well as a window for detected waypoints will show up
- WASD to navigate up, left, down, and right respectively if running main.ipynb
## Scenarios
Agent must:
- avoid collision with walls/stay on the road
- stay on the right side of the road
- stop at traffic lights or stop signs
- slow down at yield signs
- avoid collision with other random acting agent cars
- avoid collision with random pedestrians

## Creating Maps
- make sure it is 900x500 in dimension
- anything black RGB(0,0,0) will be indentified as a collision
- blue circle RGB(0,0,255) will be identified as a waypoint and used as a reward
- Put into the assets folder as a .png file. Then go to the desired .ipynb file to load it in. Will be assigned to the `MAP_IMAGE` variable

## Issues
- Need more fine tuning of hyperparameters and need to train the model for longer
- The current way of setting waypoints does not specify direction

## Dependencies
- Python3.8
- Use jupyter notebook
    - Dependencies for the Q-learning file are installed in the first code block
- Reccomend using a virtual environment
- TODO: I need to clean up the requirements file, for now this will have to do
    - `pip install -r requirements.txt`
        - `pip install --upgrade pip` if package is not found