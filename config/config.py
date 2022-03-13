from lib2to3.pgen2.token import STAR
from math import pi
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
'''
class Car(object):
    def __init__(self):
        self.x          = STARTX
        self.y          = STARTY
        self.ang        = ANGLE
        self.vel        = VEL
        self.acc        = ACC
        self.w          = W
        self.width      = CAR_WIDTH
        self.height     = CAR_HEIGHT
    
    def reset(self):
        self.x          = STARTX
        self.y          = STARTY
        self.ang        = ANGLE
        self.vel        = VEL
        self.acc        = ACC
        self.w          = W
