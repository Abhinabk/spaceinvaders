import pygame
import random
import math
pygame.mixer.init()
pygame.init()
clock = pygame.time.Clock()
# size of the window
HEIGHT = 800  # y axis
WEIDTH = 1000  # x axis
# creating th window
screen = pygame.display.set_mode((WEIDTH, HEIGHT))
#background sound
pygame.mixer.music.load("backgroundm.wav")
pygame.mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space invaders")
icon = pygame.image.load("space-invaders.png")
pygame.display.set_icon(icon)
# player
playerImg = pygame.image.load("player.png")
player_X = 440
player_Y = 700
playerX_change = 0
# enemy
enemyImg = []
enemy_X = []
enemy_Y = []
enemy_Xchange = []
enemy_Ychange = []
no_of_enemy = 6
for i in range(no_of_enemy):
    enemyImg.append(pygame.image.load("skull.png"))
    enemy_X.append(random.randint(0, 935))
    enemy_Y.append(random.randint(50, 200))
    enemy_Xchange.append(4)
    enemy_Ychange.append(40)
# bullet
# ready the bullet cant be seen
# fire state the bullet fires
bulletImg = pygame.image.load("bullet.png")
bullet_X = 0
bullet_Y = 700  # y will always remain fix the top of the spacecraft
bullet_Ychange = 15
bullet_state = "ready"

# background image
pic = pygame.image.load("background1.png")
pic = pygame.transform.scale(pic, (WEIDTH, HEIGHT))
#sore count
score_value = 0
font = pygame.font.Font("freesansbold.ttf",32)
textX = 10
textY = 10
gameFont = pygame.font.Font("freesansbold.ttf",64)
running = True
# displays the player
def Score(x,y):
    score = font.render("Score:"+str(score_value),True,(255,255,255))
    screen.blit(score, (x, y))

def gameOver():
    game = gameFont.render("Game Over:"+str(score_value),True,(255,255,255))
    screen.blit(game, (250,350))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y,i):
    screen.blit(enemyImg[i], (x, y))


def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemy_X,enemy_Y,bullet_X,bullet_Y):
    distance = math.sqrt((math.pow(enemy_X-bullet_X,2))+(math.pow(enemy_Y-bullet_Y,2)))
    if distance < 27: #pixel count
        return True
    return False


# main loop
while running:
    screen.fill((0, 0, 0))
    # background image
    screen.blit(pic, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_change = -5
            if event.key == pygame.K_d:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                bulletSound = pygame.mixer.Sound("laser.wav")
                bulletSound.play()
                if bullet_state is "ready":
                    bullet_X = player_X #withos this the bullet will follow the spaceship
                    bullet(bullet_X,bullet_Y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or pygame.K_d:
                playerX_change = 0
    # player boundary check
    player_X += playerX_change
    if player_X <= 0:
        player_X = 0
    elif player_X >= 936:
        player_X = 936
    # enemy movement
    for i in range(no_of_enemy):
        #game over mechanism
        if enemy_Y[i] >=640: #pixel count of the spacecraft - spaceX
            for j in range(no_of_enemy):
                enemy_Y[j] = 2000
            gameOver()
            break
        enemy_X[i] += enemy_Xchange[i]

        if enemy_X[i] <= 0:
            enemy_Xchange[i] = 4
            enemy_Y[i] += enemy_Ychange[i]
        elif enemy_X[i] >= 936:
            enemy_Xchange[i] = -4
            enemy_Y[i] += enemy_Ychange[i]
        #collision
        coll = isCollision(enemy_X[i],enemy_Y[i],bullet_X,bullet_Y)
        if coll:
            collSound = pygame.mixer.Sound("explosion.wav")
            collSound.play()
            bullet_Y  = 700
            bullet_state = "ready"
            score_value+=10
            enemy_X[i] = random.randint(0, 935)
            enemy_Y[i] = random.randint(50, 200)

        enemy(enemy_X[i], enemy_Y[i],i)

    
    #bullet movement
    #without this the bullet will not continue to travel
    if bullet_Y<=0:
        bullet_Y=700
        bullet_state= "ready"


    if bullet_state is "fire":
        bullet(bullet_X,bullet_Y)
        bullet_Y -= bullet_Ychange
    

    player(player_X, player_Y)
    Score(textX,textY)
    pygame.display.update()

