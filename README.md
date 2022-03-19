# SDC-RL
Testing Reinforcement Learning for Self-Driving Cars in Urban Environments using Pygame

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
- blue circle RGB(0,0,255) will be identified as a waypoint

## Dependencies
- Python3.8
- Reccomend using a virtual environment
- `pip install -r requirements.txt`
    - `pip install --upgrade pip` if package is not found

/usr/share/man/man7/libcudart.so.7.gz
/usr/lib/x86_64-linux-gnu/libcudart.so.9.1.85
/usr/lib/x86_64-linux-gnu/libcudart.so
/usr/lib/x86_64-linux-gnu/libcudart.so.9.1