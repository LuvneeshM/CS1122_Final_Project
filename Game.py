import pygame
import random
from Design import *
from Monster import AMonster
from Player import User
from Pickups import *
from Bomb import HiddenBomb

#will initialize all modules
#have to have it
pygame.init()

#need to make a canvas
#requires a tuple (aka the size of windows)
gameDisplay = pygame.display.set_mode((Layout.SCREEN_WIDTH,Layout.SCREEN_HEIGHT))
pygame.display.set_caption('BestNameEver!')

gameExit = False

#current level
level = 0

#time for frames per sec
clock = pygame.time.Clock()
framesPerSec = 60

#player
player = User()

#list of monsters
monsterList = []

#list of health packs
healthPackList = []

#list of ammo packs
ammoPackList = []

#list of hidden bombs
hiddenBombList = []
explosionAnimationList = []

#display level
font = pygame.font.SysFont("comicsansms", 16)

#spawn monsters
def spawnMonsters():
    #insert monsters
    value = level
    for i in reversed(range(len(MonsterConstants.MONSTERLEVEL))):
        for j in range(int(value/MonsterConstants.MONSTERLEVEL[i])):
            monsterList.append(AMonster(monsterList,player,i))
        value %= MonsterConstants.MONSTERLEVEL[i]
    ammoPackList.append(AmmoPickUp(random.randint(PickupConstants.WIDTH/2+Layout.BORDEROFFSET,Layout.SCREEN_WIDTH-Layout.BORDEROFFSET-PickupConstants.WIDTH/2),random.randint(PickupConstants.HEIGHT/2+Layout.TOPOFFSET,Layout.SCREEN_HEIGHT-Layout.BORDEROFFSET-PickupConstants.HEIGHT/2)))

#create hidden bombs
def createHiddenBombs(howmany):
    del hiddenBombList[:]
    for i in range(0, howmany):
        hiddenBombList.append(HiddenBomb(player))

#mouse
mouseX = 0
mouseY = 0

#shoot mode TOGGLE with key R
shoot = True

#hide cursor
pygame.mouse.set_visible(False)

#cursor image
cursorImage = pygame.transform.scale(pygame.image.load(GameImages.CURSORIMAGE).convert_alpha(),(Layout.MOUSEDIMENSIONS,Layout.MOUSEDIMENSIONS))
#background image
backGroundImage = pygame.transform.scale(pygame.image.load(GameImages.BACKGROUNDIMAGE).convert_alpha(),(Layout.SCREEN_WIDTH,Layout.SCREEN_HEIGHT))

while not gameExit:
    #no monsters left
    if len(monsterList) == 0:
        level+=1
        spawnMonsters()
        if level >= BombConstants.MINLEVEL:
            createHiddenBombs(1) # Just one bomb for now
    
    #they take care of event handling
    #i.e. if arrow key is pressed, space bar is pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        
        #Using Keypad to move
        if event.type == pygame.KEYDOWN:
            #left or right
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.leftTrue()
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.rightTrue()
            #up or down
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.upTrue()
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.downTrue()
            if event.key == pygame.K_r:
                shoot = not shoot
        #shoot bullet via mouse
        if event.type == pygame.MOUSEBUTTONDOWN and shoot == True:
            player.shootBullet(0)
        #shoot bullet via spacebar
        elif event.type == pygame.KEYDOWN and shoot == False:
            if event.key == pygame.K_SPACE:
                player.shootBullet(1)
        if event.type == pygame.KEYUP:
            #player should stop moving
            #in said direction
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.leftFalse()
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.rightFalse()
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.upFalse()
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.downFalse()

    #check collisions, game logic stuff
    #update graphcs to screen

    #make the color of the screen
    #will always be first
    #gameDisplay.fill(Color.ANTIQUEWHITE)
    gameDisplay.blit(backGroundImage,[0,0,Layout.SCREEN_WIDTH,Layout.SCREEN_HEIGHT])
    
    #update monsters
    for aMonster in monsterList:
        aMonster.checkBulletHitList(player.bulletList)
        if aMonster.update(monsterList,player,gameDisplay,healthPackList,ammoPackList,hiddenBombList,explosionAnimationList):
            aMonster.drawUpdate(gameDisplay)
    
    #update heealth packs
    for healthPack in healthPackList:
        healthPack.drawUpdate(gameDisplay)
    
    #update ammo packs
    for ammoPack in ammoPackList:
        ammoPack.drawUpdate(gameDisplay)
    
    #update the player
    player.update(healthPackList,ammoPackList,hiddenBombList,explosionAnimationList)
    if player.drawUpdate(gameDisplay, framesPerSec):
        print "_________________________________________GG WP_________________________________________"
        print "Level: " + str(level)
        print "Monsters killed : " + str(player.killCount)
        print "\n\n\n\n\n\n\n\n"
        break
    
    #play explosion animations
    for anim in explosionAnimationList:
        anim.drawUpdate(gameDisplay, framesPerSec)
    
    #display level
    if player.ammo > 0:
       text = font.render(" Level:"+str(level)+" Ammo:"+str(player.ammo)+" ",True,Color.ANTIQUEWHITE,Color.GREY)
    else:   
        text = font.render(" Level:"+str(level)+" No Ammo"+" ",True,Color.RED,Color.GREY)
    gameDisplay.blit(text,[10,0,0,Layout.TOPOFFSET]) 
    
    #another way to draw rectangle
    #gameDisplay.fill(RED, rect=[200,200,50,50])
    #Using Mouse to Move
    (mouseX, mouseY) = pygame.mouse.get_pos()
    gameDisplay.blit(cursorImage,[mouseX-Layout.MOUSEDIMENSIONS/2,mouseY-Layout.MOUSEDIMENSIONS/2,Layout.MOUSEDIMENSIONS,Layout.MOUSEDIMENSIONS])
    pygame.display.update()
    
    #frames per sec, try to avoid changing this in code, keep it as a const
    clock.tick(framesPerSec) 

# unnitializing pygame
pygame.quit()
# leave python
quit()
