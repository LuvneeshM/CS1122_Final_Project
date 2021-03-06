import pygame
import math
import random
from Design import *

class Bullet:
  def __init__(self, x_coord, y_coord, angle): #x and y coords should just be player's coords, since it is shot out of the player
    self.x_coord = x_coord
    self.y_coord = y_coord
    self.angle = -math.radians(angle - 135) #angle needs to be calculated by the player when it calls shootBullet()
    self.speed = (10*math.cos(self.angle), 10*math.sin(self.angle))
    # self.speed = (1,1)
    self.isOffScreen = False
    
  def drawUpdate(self, gameDisplay): #moves the bullet according to velocity, then draws it
    if self.x_coord > Layout.SCREEN_WIDTH or self.x_coord < 0 or self.y_coord > Layout.SCREEN_HEIGHT or self.y_coord < 0: #checks if bullet is off screen
      self.isOffScreen = True #this is here so player knows it can be deleted from the player's bulletList
    else:
      self.x_coord += self.speed[0]
      self.y_coord += self.speed[1]
      pygame.draw.circle(gameDisplay, Color.GREEN, [int(round(self.x_coord)), int(round(self.y_coord))], 5, 3)
    
  def remove(self):
    self.isOffScreen = True # We may have a more elegant way of doing this later.
