import pygame
import random
import math

#To handle music
from pygame import mixer
#Initialization with pygame
pygame.init()

#background image
background=pygame.image.load('Background_Image.jpg')

#Background music
mixer.music.load('background.wav')
mixer.music.play(-1)

#creating Screen with pygame
screenWidth=800
screenHeight=600
screen=pygame.display.set_mode((screenWidth,screenHeight))

#Changing the caption
pygame.display.set_caption("Space Invaders")

#Changing the icon
icon=pygame.image.load('alien.png')
pygame.display.set_icon(icon)

#Importing the player image
playerImg=pygame.image.load('space-invaders.png')
playerX=370
playerY=480

#Importing the enemy image
enemyImg=[]
enemyX=[]
enemyY=[]
enemyY_change=[]
enemyX_change=[]
num_of_enemies=6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyY_change.append(10)
    enemyX_change.append(4)

#Importing the bullet image
bulletImg=pygame.image.load('bullet.png')
bulletX=0
bulletY=480
bulletY_change=-10
bullet_state= "ready" #This is the is_fired condition to iterate over our code

#Drawing the player image on screen
def player(playerX,playerY):
    screen.blit(playerImg,(playerX,playerY))

#Drawing the enemy image on screen
def enemy(enemyX,enemyY,i):
    screen.blit(enemyImg[i],(enemyX[i],enemyY[i]))

#Firing the bullet
def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg,(x+16,y-15))

#Condition for collision
def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    return distance<32

#Initializing the score
score_value=0
font=pygame.font.Font('freesansbold.ttf',50)

textX=10
textY=10

def show_score(x,y):
    score=font.render("Score : "+str(score_value),True,(2,255,255))
    screen.blit(score,(x,y))
#Making a condition for while loop to run and stop.
running=True

#Game Over Text
over_font=pygame.font.Font('freesansbold.ttf',75)
def game_over_text():
    over_text=over_font.render("GAME OVER",True,(2,255,255))
    screen.blit(over_text,(100,250))

#Main Game Loop, For anything to become last long we have to do inside this infinite loop.
while running:
    #Changing the background
    screen.fill((0,0,0))

    #Adding BG image
    screen.blit(background,(0,0))
    #Initialization of playerX_change to 0
    playerX_change=0
    #Iterating over all pygame events.
    for event in pygame.event.get():
        #if the top right cross button is pressed or not
        if event.type==pygame.QUIT:
            running=False

    #Taking the keyboard input!
    keys=pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and playerX>0:
        playerX_change=-5
    #width of ship=64px
    if keys[pygame.K_RIGHT] and playerX<screenWidth-64:
        playerX_change=5
    if keys[pygame.K_SPACE]:
        #If the bullet is not fired then only we can fire the bullet
        if bullet_state == "ready":
            bullet_sound=mixer.Sound('laser.wav')
            bullet_sound.play()
            bulletX=playerX #Firing position of the bullet is determined by the X-coOrdinate of the spaceship
            fire_bullet(bulletX,bulletY)

    #Player_movement
    playerX+=playerX_change

    #Enemy movement
    for i in range(num_of_enemies):
        #Game-over
        if enemyY[i]>360:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break


        enemyX[i]+=enemyX_change[i]
        #Enemy Borderization
        if enemyX[i]<=0:
            enemyX_change[i]=4
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i]>=screenWidth-64:
            enemyX_change[i]=-4
            enemyY[i]+=enemyY_change[i]

        #Collision
        collision=isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            collision_sound=mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY=playerY
            bullet_state= "ready"
            score_value+=1
            enemyX[i]=random.randint(0,735)
            enemyY[i]=random.randint(50,150)


        enemy(enemyX,enemyY,i)

    #bullet_movement
    if bulletY<=0:
        bulletY=playerY  #bulletY is always related to player y
        bullet_state= "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY+=bulletY_change


    player(playerX,playerY)

    show_score(textX,textY)

    #Updating the window after every while loop circle
    pygame.display.update()
