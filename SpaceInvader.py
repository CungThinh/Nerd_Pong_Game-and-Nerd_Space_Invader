from xmlrpc.server import MultiPathXMLRPCServer
import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Fight")
pygame.display.set_icon(pygame.image.load("spaceship.png"))
background = pygame.image.load('14658088_5509862.jpg')
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

#Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)
# minus -1 is play looping

#score
Score_font = pygame.font.Font('freesansbold.ttf',32)
def showScore(x,y):
    score = Score_font.render("Score : "+str(score_value),True,'white')
    screen.blit(score,(x,y))

#game over text
gameOver_font = pygame.font.Font('freesansbold.ttf',64)
def game_over_text(x,y):
    gameOver = gameOver_font.render("Game Over!",True,'white')
    screen.blit(gameOver,(x,y))
    
#player
playerX = 370
playerY = 480
playerX_change = 0

#enemy
num_of_enemies = 6
enemyX = []
enemyY =[]
enemyX_change = []
enemyY_change = []
for i in range (num_of_enemies):
    enemyX.append(random.randint(64,736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

#bullet
bulletX = 0
bulletY = 480   
bulletX_change  = 0
bulletY_change = 1
bullet_state = "ready"

def player(x,y):
    screen.blit(pygame.image.load('arcade-game.png'), (x,y))

def enemy(x,y):
    screen.blit(pygame.image.load('alien.png'), (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(pygame.image.load('bullet.png'),(x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if(distance < 27):
        return True
    else: 
        return False 

running = True
while running:
    screen.fill((0, 0, 0))
    #background image
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    
    playerX += playerX_change

    if playerX >= 736 :
        playerX = 736
    if playerX <= 0 :
        playerX = 0

    for i in range (num_of_enemies):

        #game over
        if enemyY[i] > 200:
            game_over_text(200,250)
            break
        if enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
        if enemyX[i] <= 0 :
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        enemyX[i] += enemyX_change[i]
        enemy(enemyX[i],enemyY[i])
        #collision
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value +=1
            enemyX[i] = random.randint(64,736)
            enemyY[i] = random.randint(50,150)
        

    #Bullet movement

    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480  
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change
    
    showScore(textX,textY)
    player(playerX, playerY)
    pygame.display.update()



