import pygame
import math

class Bullet:
  def __init__(self, x_coord, y_coord, angle): #x and y coords should just be player's coords, since it is shot out of the player
    self.x_coord = x_coord
    self.y_coord = y_coord
    self.angle = angle #angle needs to be calculated by the player when it calls shootBullet()
    self.speed = (5*math.cos(self.angle), 5*math.sin(self.angle))
    
  def drawUpdate(self, gameDisplay): #moves the bullet according to velocity, then draws it
    if self.x_coord < 800 and self.y_coord < 600: #checks if bullet is off screen
      self.x_coord += self.speed[0]
      self.y_coord += self.speed[1]
      pygame.draw.circle(gameDisplay, Color.black, [x_coord, y_coord, 10, 10], 3)
    else:
      self.kill()
    
