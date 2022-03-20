# SDC-RL
Testing Reinforcement Learning for Self-Driving Cars in Urban Environments using Pygame

Used Deep-Q network model to train our agent. See [Creating Maps](#creating-maps) to learn how to make custom maps. 

## Usage
- Download the file to a jupyter notebook environment. The VScode extension worked well for me
- On launch a window showing the detected lines as well as a window for detected waypoints will show up
- WASD to navigate up, left, down, and right respectively if running main.ipynb
### Files
- `main.ipynb` is primarily for human teleoperation and fun
- `sdcDQL.ipynb` is to run the Deep-Q RL model
    - The code should be well documented
- Trained models are saved in to the `models` folder
- `config.py` holds many of the parameters
### Car Parameters
- We can tune the linear acceleration, angular velocity, max speed, friction force on the car, and more
- Found in `config.py`
## Scenarios
Agent must:
- Avoid collision with walls/stay on the road
- Stay on the right side of the road
- Stop at traffic lights or stop signs
- Slow down at yield signs
- Avoid collision with other random acting agent cars
- Avoid collision with random pedestrians

## Creating Maps
- Make sure it is 900x500 in dimension
- Anything black RGB(0,0,0) will be indentified as a collision
- Blue circle RGB(0,0,255) will be identified as a waypoint and used as a reward
- Put into the assets folder as a .png file. Then go to the desired .ipynb file to load it in. Will be assigned to the `MAP_IMAGE` variable

## Issues
- Need more fine tuning of hyperparameters and need to train the model for longer
- The current way of setting waypoints does not specify direction
- Perhaps define the DQN paramters in config.py

## Dependencies
- Python3.8
- Use jupyter notebook
    - Dependencies for the Q-learning file are installed in the first code block
- Reccomend using a virtual environment
- TODO: I need to clean up the requirements file, for now this will have to do
    - `pip install -r requirements.txt`
        - `pip install --upgrade pip` if package is not found
