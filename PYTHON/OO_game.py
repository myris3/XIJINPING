import pygame
import random as r

class GravityObject:

    def __init__(self, x, y, radius=2, speedX=0, speedY=0, color = (0,0,0), shape=0):
        self.x = x
        self.y = y
        self.mass = 3*radius**2
        self.radius = radius
        self.speedX = speedX
        self.speedY = speedY
        self.color = color
        self.shape=0
class Ship(GravityObject):
    def __init__(self, x, y, radius=2, speedX=0, speedY=0, color=(0,255,0), shape=1):
        super().__init__(x, y, radius, speedX, speedY, color, shape)

    def moveUp(self):
        self.speedY += -1

    def moveDown(self):
        self.speedY += 1
    def moveRight(self):
        self.speedX += 1
    def moveLeft(self):
        self.speedX +=-1
class GameWorld:
    def __init__(self, object_list, screen):
        self.object_list=object_list
        self.screen = screen
    def gravity(self,mass1, mass2, distance):
            return 0.1*mass1*mass2/(distance**2)
            #return 1
    def drawAll(self):
        for item in self.object_list:
            if item.shape==0:

                pygame.draw.circle(self.screen, item.color, (round(item.x), round(item.y)), item.radius)
            elif item.shape==1:
                pygame.draw.polygon(self.screen, item.color, [(round(item.x-item.radius),round(item.y)),(round(item.x), round(item.y-item.radius)),(round(item.x+item.radius),round(item.y))])
    def updateAll(self):
        for item in self.object_list:
            for obj in self.object_list:
                if item != obj:
                    x_dist = item.x - obj.x
                    y_dist = item.y - obj.y
                    direction_x=0
                    direction_y=0
                    if x_dist <0:
                        direction_x = 1
                    else:
                        direction_x = -1
                    if y_dist <0:
                        direction_y = 1
                    else:
                        direction_y = -1

                    if abs(x_dist)<item.radius and abs(y_dist)<item.radius:
                        x_dist = item.radius
                        y_dist = item.radius
                    item.speedX += direction_x*self.gravity(item.mass, obj.mass, x_dist)/item.mass
                    item.speedY += direction_y*self.gravity(item.mass,obj.mass,x_dist)/item.mass

                    item.x += item.speedX
                    item.y += item.speedY



    def add(obj):
        self.object_list.append(obj)
    def remove(obj):
        self.object_list.remove(obj)

def run():
    pygame.init()
    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
     
    pygame.init()
     
    # Set the width and height of the screen [width, height]
    size = (700, 500)
    screen = pygame.display.set_mode(size)
     
    pygame.display.set_caption("My Game")
     
    # Loop until the user clicks the close button.
    done = False
    objects = []
    a_num = 0
    for i in range(0,a_num):
        objects.append(GravityObject(x=size[0]*r.random(), y=size[1]*r.random(), radius=2+round(5*r.random())))
    sun = GravityObject(x=100, y=100, radius=20, color=RED )
    player = Ship(x=200, y=200, radius=5)
    objects.append(sun)
    objects.append(player)
    world = GameWorld(objects,screen)
    


    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
     
            elif event.type == pygame.KEYDOWN:
                # Figure out if it was an arrow key. If so
                # adjust speed.
                if event.key == pygame.K_LEFT:
                    player.moveLeft()
                elif event.key == pygame.K_RIGHT:
                    player.moveRight()
                elif event.key == pygame.K_UP:
                    player.moveUp()
                elif event.key == pygame.K_DOWN:
                    player.moveDown()
     
                   # --- Game logic should go here
        world.updateAll()
        # --- Screen-clearing code goes here
     
        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
     
        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(WHITE)
        
        # --- Drawing code should go here
        world.drawAll()
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
     
        # --- Limit to 60 frames per second
        clock.tick(30)
     
    # Close the window and quit.
    pygame.quit()
if __name__=="__main__":
    run()

