from math import pi
from gym import Env, spaces
'''
Define parameters for Deep Q-learning
-----------
num_iterations: number of interations
initial_collect_steps:
collect_steps_per_iteration:
replay_buffer_max_length:
batch_size:
learning_rate:
log_interval:
'''
NUM_ITERATIONS              = 20000      
INITIAL_COLLECT_STEPS       = 100 
COLLECT_STEPS_PER_ITERATION = 1
REPLAY_BUFFER_MAX_LENGTH    = 100000
BATCH_SIZE                  = 64 
LEARNING_RATE               = 1e-3
LOG_INTERVAL                = 200

'''
Here we define constant values as to make main.py cleaner
-----------
WIDTH, HEIGHT:  The dimensions of the screen drawn
STARTX, STARTY: Starting position of the car
ANGLE:          Starting angle for the car
FPS:            Frames per second of simulation
VEL:            Starting velocity of vehicle in meters/second
ACC:            Starting acceleration of the vehicle in meters/second^2
ANGULAR_ACC:    Angular Acceleation in radians/second^2
CAR_WIDTH:      Width of Car in 2D
CAR_HEIGHT:     Height of Car in 2D

FRICTION:       Friction term to simulate friction

Various RGB colors and their values in 3-tuples or 4-tuples if RGBA
'''
WIDTH, HEIGHT   = 900, 500
STARTX, STARTY  = WIDTH/2, HEIGHT-50
ANGLE           = 0.
FPS             = 60
VEL             = 0.
VEL_MAX         = 5
ACC             = 0.05
W               = pi/60.
CAR_WIDTH       = 15
CAR_HEIGHT      = 30

FRICTION        = 0.01

WHITE           = (255, 255, 255)
BLACK           = (0, 0, 0)
GREEN           = (0, 255, 0)
BLUE            = (0, 0, 255)
RED             = (255, 0, 0)
SOFT_RED        = (238, 78, 78)
MAGENTA         = (235, 105, 243)
ORANGE          = (255, 160, 47)


WHITEALPHA      = (255, 255, 255, 255)

'''
Car class to access and store all variables related to the car
------------
x,y:    True x,y pose of car
ang:    Angle of the car in radians
vel:    Float indicating velocity
acc:    Float indicating acceleration
w:      Angular velocity 
wdot:   Angular Acceleration in rad/s
width:  Width of car in 2D
height: Height of car in 2D
reward: Reward for Q-Learning
num_laserscan:  number of lasers
laserscan_dist: Max distance of simulation laser scan
'''
class Car(object):
    def __init__(self):
        self.x              = STARTX
        self.y              = STARTY
        self.ang            = ANGLE
        self.vel            = VEL
        self.acc            = ACC
        self.w              = W
        self.width          = CAR_WIDTH
        self.height         = CAR_HEIGHT
        self.reward         = 0.
        self.action_space   = spaces.Discrete(10,)
        #self.observation    = array([self.x, self.y, self.vel, self.ang])
        self.num_laserscan  = 12
        self.laserscan_dist = 100
    
    '''
    For Q learning
    '''
    def get_action_meanings(self):
        return {0: "Left",
                1: "Right",
                2: "Forward",
                3: "Backward",
                4: "Forward Left",
                5: "Forward Right",
                6: "Backward Left",
                7: "Backward Right",
                8: "Nothing"}
    

    def reset(self):
        self.x          = STARTX
        self.y          = STARTY
        self.ang        = ANGLE
        self.vel        = VEL
        self.acc        = ACC
        self.w          = W
        self.reward     = 0.
