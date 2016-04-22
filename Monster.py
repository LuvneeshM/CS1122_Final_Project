import pygame
import random
from Design import *

class AMonster:

    #constructor
    def __init__(self,monsterList):
        #health
        self.currentHealth = 3
        self.maxHealth = 3
        #dimensions
        self.monsterWidth = 50
        self.monsterHeight = 50
        #movement frequency
        self.delayTimer = 15
        self.delay = 0
        #movement shift
        self.monsterMoveRate = 20
        #possible movement rates
        self.movements = [(0,-self.monsterMoveRate),(0,self.monsterMoveRate),(-self.monsterMoveRate,0),(self.monsterMoveRate,0)]
        
        #random spawn location
        self.monsterX = random.randint(self.monsterWidth/2+Layout.borderOffSet,Layout.screen_width-Layout.borderOffSet-self.monsterWidth/2)
        self.monsterY = random.randint(self.monsterHeight/2+Layout.topOffSet,Layout.screen_height-Layout.borderOffSet-self.monsterHeight/2)
        i = 0
        while i < len(monsterList):
            if monsterList[i].checkMonsterRect(self.monsterX,self.monsterY):
                i = -1
                self.monsterX = random.randint(self.monsterWidth/2+Layout.borderOffSet,Layout.screen_width-Layout.borderOffSet-self.monsterWidth/2)
                self.monsterY = random.randint(self.monsterHeight/2+Layout.topOffSet,Layout.screen_height-Layout.borderOffSet-self.monsterHeight/2)
            i+=1
        #represents the image
        self.imageSurface = pygame.transform.scale(pygame.image.load(GameImages.monsterImage).convert_alpha(),(self.monsterWidth,self.monsterHeight))
        
    #update monster position
    def update(self):
        if self.currentHealth <= 0:
            # The monster is dead.
            return False
        if self.delay == self.delayTimer:
            #random movement
            pair = self.movements[random.randint(0,len(self.movements)-1)]
            #CHECKS THE BORDER BOUNDARIES 
            self.monsterX += pair[0]
            if self.monsterX > Layout.screen_width-self.monsterWidth/2-Layout.borderOffSet:
                self.monsterX = Layout.screen_width-self.monsterWidth/2-Layout.borderOffSet
            elif self.monsterX < self.monsterWidth/2+Layout.borderOffSet:
                self.monsterX = self.monsterWidth/2+Layout.borderOffSet
            self.monsterY += pair[1]
            if self.monsterY > Layout.screen_height-self.monsterHeight/2-Layout.borderOffSet:
                self.monsterY = Layout.screen_height-self.monsterHeight/2-Layout.borderOffSet
            elif self.monsterY < self.monsterHeight/2+Layout.topOffSet:
                self.monsterY = self.monsterHeight/2+Layout.topOffSet
        self.delay += 1
        #resets delay
        if self.delay > self.delayTimer:
           self.delay = 0 
        return True
        
    def drawUpdate(self, gameDisplay):
        #monster display
        gameDisplay.blit(self.imageSurface,[self.monsterX - self.monsterWidth/2,self.monsterY - self.monsterHeight/2,self.monsterWidth,self.monsterHeight])
        #health bar
        pygame.draw.rect(gameDisplay,Color.red if self.currentHealth/self.maxHealth > .5 else Color.darkred if self.currentHealth/self.currentHealth > .25 else Color.grayish,[(self.monsterX - self.monsterWidth/2)+self.monsterWidth*(1-(self.currentHealth/float(self.maxHealth))),self.monsterY - self.monsterHeight/2,self.monsterWidth*(self.currentHealth/float(self.maxHealth)),2])
        
    def gotHitByBullet(self):
        self.currentHealth -= 1
        
    def checkBulletHit(self, bullet):
        # Checks whether this monster was hit by a bullet
        if abs(bullet.x_coord - self.monsterX) <= self.monsterWidth / 2 and abs(bullet.y_coord - self.monsterY) <= self.monsterHeight / 2:
            # The bullet hit the monster!
            self.gotHitByBullet()
            bullet.remove()
            return True
        return False
       
    def checkBulletHitList(self, bulletList):
        for bullet in bulletList:
            if self.checkBulletHit(bullet):
                break
                
    def checkMonsterRect(self,monsterX,monsterY):
        if self.monsterX - self.monsterWidth/2 <= monsterX and self.monsterX + self.monsterWidth/2 >= monsterX:
            return True
        return False