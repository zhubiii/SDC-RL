import pygame
import sys, os
from math import *
sys.path.append("./config/")
import config
from config import Car

# Specify which map
map = 'map1.png'

# Init Car object
Car = Car()
# Initialize the window
WIN = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption('SDC-RL')

# Initalize fonts for text
pygame.font.init()
REWARD_FONT = pygame.font.SysFont('comicsans', 30)

# Load in map of our choosing
MAP_IMAGE = pygame.image.load(os.path.join('Assets', map)).convert_alpha()

# Initialize the car image
# Convert converts to pixel and speeds up runtime
CAR_IMAGE = pygame.image.load(os.path.join('Assets', 'car.png')).convert_alpha()
# Car starts facing positive x-axis
CAR_IMAGE = pygame.transform.rotate(pygame.transform.scale(CAR_IMAGE, (Car.width, Car.height)), -90)

# Define all the event IDs
OFFROAD = pygame.USEREVENT+1

'''
Function to handle the movement inputs of the car
WASD controls for Drive Forward, Turn Left, Drive Backward, and Turn Right, respectively
Turning Left or Right requires a redrawing of the CAR_IMAGE

Params:
-------
keys_pressed:   allows us to know which keys were pressed, even multiple at a time
game_car:    Takes in the pygame rectangle representing our car

Returns:
--------
Nothing
'''
def handle_movement(keys_pressed, game_car):
    if keys_pressed[pygame.K_a]:  # LEFT
        Car.ang     -= Car.w
    if keys_pressed[pygame.K_d]:  # RIGHT
        Car.ang     += Car.w
    if keys_pressed[pygame.K_w]:  # UP
        Car.vel     += Car.acc
    if keys_pressed[pygame.K_s]:  # DOWN
        Car.vel     -= Car.acc


'''
Function to redraw the window for each game loop

Params:
-------
game_car:    Takes in the pygame rectangle representing our car


Returns:
--------
Nothing
'''
def draw_window(game_car, image, keys_pressed, reward):
    # Draw background
    WIN.blit(MAP_IMAGE, (0,0))
    # Draw reward text
    reward_text = REWARD_FONT.render("Reward: "+str(reward), 1, config.BLACK)
    WIN.blit(reward_text, (config.WIDTH - reward_text.get_width()-10, 10))
    # Draw input indicators
    if keys_pressed[pygame.K_a]:  # LEFT
        pygame.draw.circle(WIN, (200, 0, 250), [config.WIDTH/2-50,config.HEIGHT/2], 15, 0)
    else:
        pygame.draw.circle(WIN, (200, 0, 250), [config.WIDTH/2-50,config.HEIGHT/2], 15, 3)
    if keys_pressed[pygame.K_d]:  # RIGHT
        pygame.draw.circle(WIN, (200, 0, 250), [config.WIDTH/2+50,config.HEIGHT/2], 15, 0)
    else:
        pygame.draw.circle(WIN, (200, 0, 250), [config.WIDTH/2+50,config.HEIGHT/2], 15, 3)
    if keys_pressed[pygame.K_w]:  # UP
        pygame.draw.circle(WIN, (200, 0, 250), [config.WIDTH/2,config.HEIGHT/2 -50], 15, 0)
    else:
        pygame.draw.circle(WIN, (200, 0, 250), [config.WIDTH/2,config.HEIGHT/2 -50], 15, 3)
    if keys_pressed[pygame.K_s]:  # DOWN
        pygame.draw.circle(WIN, (200, 0, 250), [config.WIDTH/2,config.HEIGHT/2 +50], 15, 0)
    else:
        pygame.draw.circle(WIN, (200, 0, 250), [config.WIDTH/2,config.HEIGHT/2 +50], 15, 3)
    # Draw car
    WIN.blit(image, (game_car.x, game_car.y))
    pygame.display.update()

'''
Function that checks velocity for max velocity and adds friction damping term

Params:
-------
None

Returns:
--------
Nothing
'''
def check_velocity():
    # Check if velocity exceeds max velocity
    if Car.vel > config.VEL_MAX:
        Car.vel = config.VEL_MAX
    elif Car.vel < -config.VEL_MAX:
        Car.vel = -config.VEL_MAX
        
    # Apply friction damping term
    if Car.vel > 0:
        if Car.vel - config.FRICTION < 0:
            Car.vel = 0
        else:
            Car.vel -= config.FRICTION
    if Car.vel < 0:
        if Car.vel + config.FRICTION > 0:
            Car.vel = 0
        else:
            Car.vel += config.FRICTION

'''
Function to detect collision with walls based on color of pixels

Params:
-------
None:   We use the Car objects coordinates for the "true" value to
        avoid pixel rounding
'''
def detect_wall_collision():
    color = WIN.get_at((int(Car.x), int(Car.y)))
    if color == config.WHITEALPHA:
        pygame.event.post(pygame.event.Event(OFFROAD))

'''
Function to reset the game

Params:
-------
game_car:    Takes in the pygame rectangle representing our car
'''
def reset_game(game_car):
    game_car.x = config.STARTX
    game_car.y = config.STARTX
    Car.reset()


'''
Main function where game loop runs
'''
def main():
    # set initial pose of car in game
    # Car starts facing positive x-axis
    game_car = pygame.Rect(config.STARTX, config.STARTY, Car.width, Car.height)

    # Conditions for game loop
    clock   = pygame.time.Clock()
    run     = True
    while run:
        clock.tick(config.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # Check if car went off road
            if event.type == OFFROAD:
                reset_game(game_car)

        keys_pressed = pygame.key.get_pressed()
        handle_movement(keys_pressed, game_car)
        # rotate the vehicle
        angle_in_degrees = Car.ang*(180./pi)
        image    = pygame.transform.rotate(CAR_IMAGE, -angle_in_degrees)
        game_car = image.get_rect(center = image.get_rect(center = (Car.x,Car.y)).center)
        check_velocity()
        # We assign this way so that we dont accumulate pixel rounding error (pixels not continuous)
        Car.x  += Car.vel*cos(Car.ang)
        Car.y  += Car.vel*sin(Car.ang)
        game_car.x = Car.x
        game_car.y = Car.y

        detect_wall_collision()

        draw_window(game_car, image, keys_pressed, 1)

    pygame.quit()

    

if __name__ == "__main__":
    main()