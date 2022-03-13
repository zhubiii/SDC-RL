import pygame
import sys, os
from math import *
sys.path.append("./config/")
import config
from config import Car

# Init Car object
Car = Car()
# Initialize the window
WIN = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption('SDC-RL')

# Initialize the car image
CAR_IMAGE = pygame.image.load(os.path.join('Assets', 'car.png'))
# Car starts facing positive x-axis
CAR_IMAGE = pygame.transform.rotate(pygame.transform.scale(CAR_IMAGE, (Car.width, Car.height)), -90)


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
        Car.ang     += Car.w
    if keys_pressed[pygame.K_d]:  # RIGHT
        Car.ang     -= Car.w
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
def draw_window(game_car, image):
    WIN.fill(config.WHITE)
    WIN.blit(image, (game_car.x, game_car.y))
    pygame.display.update()

'''
Function that checks velocity for max velocity and adds friction damping term
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

        keys_pressed = pygame.key.get_pressed()
        handle_movement(keys_pressed, game_car)
        angle_in_degrees = Car.ang*(180./pi)
        image    = pygame.transform.rotate(CAR_IMAGE, -angle_in_degrees)
        game_car = image.get_rect(center = image.get_rect(center = game_car.center).center)
        check_velocity()
        print(game_car.x)
        game_car.x  += Car.vel*cos(Car.ang)
        game_car.y  += Car.vel*sin(Car.ang)

        draw_window(game_car, image)

    pygame.quit()

    

if __name__ == "__main__":
    main()