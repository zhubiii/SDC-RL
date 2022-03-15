import pygame
import cv2
import numpy as np
import sys, os
from math import *
sys.path.append("./config/")
import config
from config import Car

# Specify if we want to use RL
QLEARNING = False

# Specify which map
MAP_PATH = os.path.join('Assets', 'map1.png')


# Init Car object
Car = Car()
# Initialize the window
WIN = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption('SDC-RL')

# Initalize fonts for text
pygame.font.init()
REWARD_FONT = pygame.font.SysFont('comicsans', 30)

# Load in map of our choosing
MAP_IMAGE = pygame.image.load(MAP_PATH).convert_alpha()

# Initialize the car image
# NB: Convert converts to pixel and speeds up runtime
CAR_IMAGE = pygame.image.load(os.path.join('Assets', 'car.png')).convert_alpha()
# Car starts facing positive x-axis
CAR_IMAGE = pygame.transform.rotate(pygame.transform.scale(CAR_IMAGE, (Car.width, Car.height)), -90)

# Define all the event IDs
COLLISION = pygame.USEREVENT+1

'''
Function to find all the walls from the background image and
store them in the WALLS list

Using openCV line detection for black lines

Params:
-------
None

Returns:
--------
Coordinates of the begin/end points of each line segment that makes up each barrier
'''
def create_walls():
    print('Generating Walls...')
    # Preprocessing
    img = cv2.imread(MAP_PATH, cv2.IMREAD_COLOR)
    lower = np.array([0, 0, 0])
    upper = np.array([0, 0, 0])
    black_mask = cv2.inRange(img, lower, upper) # Isolate all black pixels
    result = 255 - black_mask

    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(result, low_threshold, high_threshold)
    dilated = cv2.dilate(edges, np.ones((3,3), dtype=np.uint8))

    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 25  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 50  # minimum number of pixels making up a line
    max_line_gap = 20  # maximum gap in pixels between connectable line segments
    line_image = np.copy(img) * 0  # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(dilated, rho, theta, threshold, np.array([]),
                        min_line_length, max_line_gap)

    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),1)
    lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
    #cv2.imshow('Edges', dilated)
    cv2.imshow('Detected Walls/Obstacles', line_image)
    cv2.waitKey(1)
    print(str(len(lines))+' lines detected')
    return lines
'''
Step function for Q-Learning
'''
def step(action):
    # TODO:
    # marks termination of episode
    done = False

    # assert this is a valid function
    assert Car.action_space.contains(action), "Invalid Action"

    # Apply Action
    handle_movementRL(action)

    # Calculate the reward
    Car.reward = 1


'''
Function for Q learning to handle movement
'''
def handle_movementRL(action):
    if action == 0:                 # LEFT
        Car.ang     -= Car.w
    if action == 1:                 # RIGHT
        Car.ang     += Car.w
    if action == 2:                 # UP
        Car.vel     += Car.acc
    if action == 3:                 # DOWN
        Car.vel     -= Car.acc
    if action == 4:                 # Forward Left
        Car.vel     += Car.acc
        Car.ang     -= Car.w
    if action == 5:                 # Forward Right
        Car.vel     += Car.acc
        Car.ang     += Car.w
    if action == 6:                 # Backward Left
        Car.vel     -= Car.acc
        Car.ang     -= Car.w
    if action == 7:                 # Backward Right
        Car.vel     -= Car.acc
        Car.ang     += Car.w
    if action == 8:
        pass
        



'''
Function to handle the movement inputs of the car
WASD controls for Drive Forward, Turn Left, Drive Backward, and Turn Right, respectively
Turning Left or Right requires a redrawing of the CAR_IMAGE

Params:
-------
keys_pressed:   Allows us to know which keys were pressed, even multiple at a time
game_car:    Takes in the pygame rectangle representing our car

Returns:
--------
Nothing
'''
def handle_movement(keys_pressed):
    if keys_pressed[pygame.K_a]:  # LEFT
        Car.ang     -= Car.w
    if keys_pressed[pygame.K_d]:  # RIGHT
        Car.ang     += Car.w
    if keys_pressed[pygame.K_w]:  # UP
        Car.vel     += Car.acc
    if keys_pressed[pygame.K_s]:  # DOWN
        Car.vel     -= Car.acc

'''
Function to draw indicators
'''
def draw_indicators(keys_pressed, action):
    if QLEARNING:
        if action == 0 or action == 4 or action == 6:  # LEFT
            pygame.draw.circle(WIN, config.MAGENTA, [config.WIDTH/2-30,config.HEIGHT/2], 15, 0)
        else:
            pygame.draw.circle(WIN, config.MAGENTA, [config.WIDTH/2-30,config.HEIGHT/2], 10, 3)
        if action == 1 or action == 5 or action == 7:  # RIGHT
            pygame.draw.circle(WIN, config.MAGENTA, [config.WIDTH/2+30,config.HEIGHT/2], 12, 0)
        else:
            pygame.draw.circle(WIN, config.MAGENTA, [config.WIDTH/2+30,config.HEIGHT/2], 10, 3)
        if action == 2 or action == 4 or action == 5:  # UP
            pygame.draw.circle(WIN, config.MAGENTA, [config.WIDTH/2,config.HEIGHT/2 -30], 12, 0)
        else:
            pygame.draw.circle(WIN, config.MAGENTA, [config.WIDTH/2,config.HEIGHT/2 -30], 10, 3)
        if action == 3 or action == 6 or action == 7:  # DOWN
            pygame.draw.circle(WIN, config.MAGENTA, [config.WIDTH/2,config.HEIGHT/2 +30], 12, 0)
        else:
            pygame.draw.circle(WIN, config.MAGENTA, [config.WIDTH/2,config.HEIGHT/2 +30], 10, 3)
    else:
        if keys_pressed[pygame.K_a]:  # LEFT
            pygame.draw.circle(WIN, config.MAGENTA, [config.WIDTH/2-30,config.HEIGHT/2], 12, 0)
        else:
            pygame.draw.circle(WIN, config.MAGENTA, [config.WIDTH/2-30,config.HEIGHT/2], 10, 3)
        if keys_pressed[pygame.K_d]:  # RIGHT
            pygame.draw.circle(WIN, config.MAGENTA, [config.WIDTH/2+30,config.HEIGHT/2], 12, 0)
        else:
            pygame.draw.circle(WIN, config.MAGENTA, [config.WIDTH/2+30,config.HEIGHT/2], 10, 3)
        if keys_pressed[pygame.K_w]:  # UP
            pygame.draw.circle(WIN, config.MAGENTA, [config.WIDTH/2,config.HEIGHT/2 -30], 12, 0)
        else:
            pygame.draw.circle(WIN, config.MAGENTA, [config.WIDTH/2,config.HEIGHT/2 -30], 10, 3)
        if keys_pressed[pygame.K_s]:  # DOWN
            pygame.draw.circle(WIN, config.MAGENTA, [config.WIDTH/2,config.HEIGHT/2 +30], 12, 0)
        else:
            pygame.draw.circle(WIN, config.MAGENTA, [config.WIDTH/2,config.HEIGHT/2 +30], 10, 3)


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
Function to detect collision with walls based on line intersection
we break our car down into four line segments and check against walls

Params:
-------
WALLS:  List of all our line segment walls

Return:
-------
Nothing
'''
def detect_wall_collision(game_car, WALLS):
    bl = ((Car.x-(cos(Car.ang)*Car.height/2)), (Car.y-(sin(Car.ang)*Car.width/2))) # back left point of car 
    fl = ((Car.x+(cos(Car.ang)*Car.height/2)), (Car.y-(sin(Car.ang)*Car.width/2))) # front left point of car 
    br = ((Car.x-(cos(Car.ang)*Car.height/2)), (Car.y+(sin(Car.ang)*Car.width/2))) # back right point of car 
    fr = ((Car.x+(cos(Car.ang)*Car.height/2)), (Car.y+(sin(Car.ang)*Car.width/2))) # front right point of car 

    front   = (fl,fr)
    back    = (bl, br)
    lside   = (fl, bl)
    rside   = (fr, br)
    car_seg = [front, back, lside, rside]

    intersection = False
    for wall in WALLS:
        for x3,y3,x4,y4 in wall:
            for seg in car_seg:
                x1 = seg[0][0]
                y1 = seg[0][1]
                x2 = seg[1][0]
                y2 = seg[1][1]
                denom  = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
                # if denom 0, lines parallel so never intersect
                if denom == 0:
                    continue
                t1  = (x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)
                t   = t1/denom
                u1  = (x1-x3)*(y1-y2) - (y1-y3)*(x1-x2)
                u   = u1/denom
                # Test to see if intersection exists
                if 0<=t and t<=1 and 0<=u and u<=1:
                    intersection = True
                    pygame.event.post(pygame.event.Event(COLLISION))
                    break # Stop checking for wall intersection if we already found one
        if intersection:
            break

'''
Function to simulate laserscan
first laser will point straight ahead of the car, then
increments by 2pi/num_laserscan 
-1 is out of range

Params:
-------
WALLS:  List of all our line segment walls

Return:
-------
List of laserscan measurements
'''
def get_laserscan(WALLS):
    num     = Car.num_laserscan
    angle   = Car.ang
    # Use line intersection formula
    x1 = Car.x
    y1 = Car.y
    laserscan = []
    for i in range(0, num):
        # All variables for Line intersection
        x2 = Car.x+(Car.laserscan_dist*cos(angle))
        y2 = Car.y+(Car.laserscan_dist*sin(angle))
        angle += ((2*pi) / num)
        intersect = False
        for wall in WALLS:
            for x3,y3,x4,y4 in wall:
                denom  = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
                if denom == 0: # if denom 0, lines parallel so never intersect
                    continue
                t1  = (x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)
                t   = t1/denom
                u1  = (x1-x3)*(y1-y2) - (y1-y3)*(x1-x2)
                u   = u1/denom
                if 0<=t and t<=1 and 0<=u and u<=1: # Test to see if intersection exists
                    Px = x1+(t*(x2-x1))
                    Py = y1+(t*(y2-y1))
                    # Calculate distance between laserscan origin and intersection
                    dist = sqrt((Px-Car.x)**2 + (Py-Car.y)**2)
                    laserscan.append(dist)
                    intersect = True
                    break # Stop checking for wall intersection if we already found one
            if intersect:
                break
        if not intersect:
            laserscan.append(-1)

    return laserscan

'''
Function to draw the laserscan in draw_window
'''
def draw_laserscan(laserscan):
    num     = Car.num_laserscan
    angle   = Car.ang
    for i in range(0, num):
        # Find the start and endline using trig (similar to forward kinematics)
        # If it equals negative 1 the full laser length is drawn
        if laserscan[i] == -1:
            pygame.draw.line(WIN, config.RED,
                            (Car.x, Car.y),
                            (Car.x+(Car.laserscan_dist*cos(angle)), Car.y+(Car.laserscan_dist*sin(angle))),
                            1)
        else:
            pygame.draw.line(WIN, config.RED,
                            (Car.x, Car.y),
                            (Car.x+(laserscan[i]*cos(angle)), Car.y+(laserscan[i]*sin(angle))),
                            1)
        angle += ((2*pi) / num)
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
Function to redraw the window for each game loop

Params:
-------
game_car:    Takes in the pygame rectangle representing our car


Returns:
--------
Nothing
'''
def draw_window(game_car, image, keys_pressed, action, laserscan):
    # Draw background
    WIN.blit(MAP_IMAGE, (0,0))
    # Draw reward text
    reward_text = REWARD_FONT.render("Reward: "+str(Car.reward), 1, config.BLACK)
    WIN.blit(reward_text, (config.WIDTH - reward_text.get_width()-10, 10))
    # Draw input indicators
    draw_indicators(keys_pressed, action)
    # Draw Walls different color
    #for wall in WALLS:
        #pygame.draw.rect(WIN, config.ORANGE, wall)

    # Draw Car hitbox
    pygame.draw.rect(WIN, config.SOFT_RED, game_car)
    # Draw the laserscan
    draw_laserscan(laserscan)
    # Draw car
    WIN.blit(image, image.get_rect(center=(Car.x, Car.y)))

    pygame.display.update()

'''
Main function where game loop runs
'''
def main():
    # set initial pose of car in game
    # Car starts facing positive x-axis
    # NB: We might not need game_car since we use line intersection for collision, will keep for now
    game_car = pygame.Rect(0, 0, Car.width, Car.height)

    # Create walls
    WALLS = create_walls()

    # Conditions for game loop
    clock   = pygame.time.Clock()
    run     = True
    action  = -1
    keys_pressed = None
    while run:
        clock.tick(config.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # Check if car went off road
            if event.type == COLLISION:
                reset_game(game_car)

        # Do not take user input if in Q learning mode
        if QLEARNING:
            # Take random action
            action = Car.action_space.sample()
            step(action)
        else:
            keys_pressed = pygame.key.get_pressed()
            handle_movement(keys_pressed)
        # rotate the vehicle
        angle_in_degrees = Car.ang*(180./pi)
        image    = pygame.transform.rotate(CAR_IMAGE, -angle_in_degrees)
        game_car = image.get_rect(center=game_car.center)
        check_velocity()
        # We assign this way so that we dont accumulate pixel rounding error (pixels not continuous)
        Car.x  += Car.vel*cos(Car.ang)
        Car.y  += Car.vel*sin(Car.ang)
        game_car.centerx = Car.x
        game_car.centery = Car.y

        detect_wall_collision(game_car, WALLS)
        laserscan = get_laserscan(WALLS)

        draw_window(game_car, image, keys_pressed, action, laserscan)

    pygame.quit()

    

if __name__ == "__main__":
    main()