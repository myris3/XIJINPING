import pygame
import sys
from pygame.locals import *
import random
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
pygame.init()
 
# Set the width and height of the screen [width, height]
size = (1000, 700)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Test_game")
 
# Loop until the user clicks the close button.
done = False
a_number=1

#[x,y], radius, mass, color, speed[x,y]
sun = [[500,300], 30,100, RED, [0,0]]

dynamics = [sun]
for i in range(0,a_number):
    asteroid = [[size[0]*random.random(), size[1]*random.random()], 5, 0.6, BLACK, [random.random()*2,random.random()*2]]
    dynamics.append(asteroid)


def drawAll(object_list):
    for item in object_list:

        pygame.draw.circle(screen, item[3], (int(item[0][0]), int(item[0][1])), item[1])
        pygame.draw.line(screen, BLACK, (int(item[0][0]),int(item[0][1])), (int(item[0][0]+item[4][0]),int(item[0][1]+item[4][1])*100 ) )
def updateAll(object_list):
    for item in object_list:
        for obj in object_list:
            if (item != obj):
                item_pos=item[0]
                obj_pos=obj[0]
                x_dist = item_pos[0]-obj_pos[0]
                y_dist = -item_pos[1]+obj_pos[1]

                item_speed=item[4]
                obj_speed = obj[4]

                item_mass=item[2]
                obj_mass=obj[2]
                
                direction_x=0
                direction_y=0
                if x_dist<0:
                    direction_x=-1
                else:
                    direction_x = 1
                if y_dist<0:
                    direction_y=-1
                else:
                    direction_y=1

                if (x_dist<item[1]):
                    x_dist=direction_x*item[1]
                if (y_dist<item[1]):
                    y_dist=direction_y*item[1]


                item_speed[0]+=direction_x*gravity(item_mass, obj_mass, x_dist)/item_mass
                item_speed[1]+=direction_y*gravity(item_mass, obj_mass, y_dist)/item_mass
                item_pos[0]+=item_speed[0]
                item_pos[1]+=item_speed[1]

                
def gravity(mass1, mass2, distance):
    return 0.01*mass1*mass2/distance**2

    



clock = pygame.time.Clock()
 
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
     
    

    
    updateAll(dynamics)

    
    screen.fill(WHITE)
    drawAll(dynamics)


    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(10)

