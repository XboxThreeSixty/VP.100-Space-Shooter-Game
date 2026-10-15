import pygame
import os
import random
import requests
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

pygame.init()

screenWidth = 1280
screenHeight = 720

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Epic Dorito Shooter: Game of the Year Edition")
screen.fill((0, 0, 0))
clock = pygame.time.Clock()

x = 75
bullets = []
enemies = []
bulletIndex = -1
magIndex = 5
playerHealth = 100
playerScore = 0
doritoBreaches = 0
username = ""
typing = False
hasSubmitted = False

R = 250
G = 0
B = 0

# Text
retro = pygame.font.Font("Retro_Gaming.ttf", 25)
bigretro = pygame.font.Font("Retro_Gaming.ttf", 50)
biggerretro = pygame.font.Font("Retro_Gaming.ttf", 100)

title = bigretro.render("EPIC DORITO SHOOTER", False, (255, 0, 0))
subtitle = retro.render("Game of the Year Edition", False, (255, 0, 0))
story = retro.render("You were hired as a bodyguard to protect the venue that Major League Gaming is\nhosting their Halo 3 tournament in but while on shift, Weegee sent his army of\ndoritos to overtake the venue and destroy Major League Gaming!!! aaa!!!!\nYou must protect the venue from the attacking dorito army at ALL COSTS!!!", False, (0, 0, 0))
titleControls = retro.render("Press Enter to make your final stand against teh doritos", False, (0, 0, 0))

ammo = retro.render("Ammo: 5/5", False, (255, 255, 255))
health = retro.render("Health: 100%", False, (0, 255, 0))
score = retro.render("Score: 0", False, (255, 0, 0))
breaches = retro.render("Doritos breached: 0", False, (0, 255, 0))

gameOverText = biggerretro.render("Game Over", False, (0, 0, 0))
restartText = retro.render("press r to restart", False, (0, 0, 0))
breachedEnd = retro.render("Too many doritos breached into the venue", False, (0, 0, 0))
healthEnd = retro.render("The doritos rekt u m8", False, (0, 0, 0))
submissionText = retro.render("(Optional) Click anywhere to start typing your username, press\nenter to submit it and your score to the leaderboard or esc to stop.", False, (0, 0, 0))
submitted = retro.render("Submitted!", False, (0, 0, 0))
nameText = retro.render("", False, (0, 0, 0))

# the big l
weegee = pygame.image.load("weegee.png").convert_alpha()
weegeeScaled = pygame.transform.scale(weegee, (50, 100))
weegeeRect = weegeeScaled.get_rect()

# Bullet
mtndew = pygame.image.load("mountaindew.png").convert_alpha()
dew = pygame.transform.scale(mtndew, (50, 50))
dew_hitbox = dew.get_rect()

# Enemy
dorito = pygame.image.load("dorito.png").convert_alpha()
dor = pygame.transform.scale(dorito, (50, 50))
dorito_hitbox = dor.get_rect()

# Player Functions
placeholderTexture = pygame.image.load("placeholder.png")
scaledPlaceholder = pygame.transform.scale(placeholderTexture, (50, 20))
placeholder = scaledPlaceholder.get_rect()

def draw_player():
    screen.fill((0, 0, 0))
    placeholder.topleft = (x, 670)

def move_player(direction):
    global x
    if direction == "left":
        if x > 0:
            x -= 8
        else:
            x -= 0
    elif direction == "right":
        if x < 1230:
            x += 8
        else: 
            x += 0

# Bullet class and Functions
class Bullet:
    def __init__(self, name, x, y, image):
        self._name = name
        self._image = image 
        self._rect = image.get_rect()
        self._rect.x = x
        self._rect.y = y
        self._fired = False
    def x(self, x):
        self._rect.x = x
    def get_x(self):
        return self._rect.x
    def y(self, y):
        self._rect.y = y
    def get_y(self):
        return self._rect.y
    def topleft(self, x, y):
        self._rect.topleft = (x, y)
    def check(self):
        return self._fired
    def changeStatus(self, bool):
        self._fired = bool

def create_bullets(bullets):
    for i in range(1, 6):
        new_bullet = Bullet(name = "bullet_" + str(i), x = 1, y = -150, image = dew.copy())
        bullets.append(new_bullet)

def draw_bullet(x, bullets, bulletIndex, magIndex):
    if magIndex >= 0:
        bullets[bulletIndex]._rect.x = x
        bullets[bulletIndex].topleft = (bullets[bulletIndex].get_x(), bullets[bulletIndex].get_y())

        if magIndex >= 0 and bullets[bulletIndex].get_y() <= -150:
            bullets[bulletIndex].y(610)

def update_bullet(i):
    bullets[i]._rect.y = bullets[i].get_y()
    if bullets[i].get_y() > -150:
        bullets[i].y(bullets[i].get_y() - 15)

# Enemy Class and Functions
class Enemy:
    def __init__(self, name, x, y, image):
        self._name = name
        self._image = image 
        self._rect = image.get_rect()
        self._rect.x = x
        self._rect.y = y
        self._alive = False
    def x(self, x):
        self._rect.x = x
    def get_x(self):
        return self._rect.x
    def y(self, y):
        self._rect.y = y
    def get_y(self):
        return self._rect.y
    def topleft(self, x, y):
        self._rect.topleft = (x, y)
    def check(self):
        return self._alive
    def changeStatus(self, bool):
        self._alive = bool

def create_enemies(enemies):
    for i in range(1, 11):
        new_enemy = Enemy(name = "enemy_" + str(i), x = random.randrange(1, 1231), y = -50, image = dor.copy())
        enemies.append(new_enemy)

def draw_enemies():
    i = random.randrange(0, 10)
    enemies[i].changeStatus(True)
    enemies[i].topleft(enemies[i].get_x(), enemies[i].get_y())
    if enemies[i].get_y() >= 720:
        enemies[i].y(-50)
        enemies[i].x(random.randrange(1, 1231))

def update_enemy(i):
    enemies[i]._rect.y = enemies[i].get_y()
    if enemies[i].get_y() < 720:
        enemies[i].y(enemies[i].get_y() + 1.5)

# Collision
def checkEnemyCollision(playerScore):
    for bullet in bullets:
        for enemy in enemies:
            collidedIndex = bullet._rect.colliderect(enemy._rect)
            if collidedIndex:
                enemy.y(800)
                bullet.y(-150)
                playerScore += 10
    return playerScore

def checkPlayerCollision(playerHealth):
    for enemy in enemies:
        collidedIndex = placeholder.colliderect(enemy._rect)
        if collidedIndex:
            enemy.y(800)
            playerHealth -= 34
            return playerHealth
    return playerHealth

# Loop to rainbowify text
def rainbowLoop(R, G, B, increment):
    if R == 250 and G < 250 and B == 0:
        G += increment

        if G > 250:
            G = 250
    elif R > 0 and G == 250 and B == 0:
        R -= increment

        if R < 0:
            R = 0
    elif R == 0 and G == 250 and B < 250:
        B += increment

        if B > 250:
            B = 250
    elif R == 0 and G > 0 and B == 250:
        G -= increment

        if G < 0:
            G = 0
    elif R < 250 and G == 0 and B == 250:
        R += increment

        if R > 250:
            R = 250
    elif R == 250 and G == 0 and B > 0:
        B -= increment

        if B < 0:
            B = 0
    return R, G, B

runningLoop = True
startMenu = True
runningGame = False
gameOver = False

create_bullets(bullets)
create_enemies(enemies)

pygame.key.set_repeat(400, 400)

# Game Loop
while runningLoop:
    while startMenu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                startMenu = False
                runningLoop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    startMenu = False
                    runningGame = True
                    R = 250
                    G = 0
                    B = 0

        title = bigretro.render("EPIC DORITO SHOOTER", False, (R, G, B))
        subtitle = retro.render("Game of the Year Edition", False, (R, G, B))
        R, G, B = rainbowLoop(R, G, B, 1)
        screen.fill((255, 255, 255))
        screen.blit(title, (300, 50))  
        screen.blit(subtitle, (460, 100)) 
        screen.blit(story, (20, 155)) 
        screen.blit(titleControls, (200, 400))
        screen.blit(weegeeScaled, weegeeRect)
        weegeeRect.topleft = (1050, 40)
        pygame.display.update()
    while runningGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runningGame = False
                runningLoop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if bulletIndex < 4:
                        bulletIndex += 1
                    elif bulletIndex == 4:
                        bulletIndex = 0
                    
                    magIndex -= 1
                    if magIndex >= 0:
                        ammo = retro.render("Ammo: "+str(magIndex)+"/5", False, (255, 255, 255))
                    draw_bullet(x, bullets, bulletIndex, magIndex)
                if event.key == pygame.K_r:
                    if magIndex != 5:
                        magIndex = 5
                        ammo = retro.render("Ammo: 5/5", False, (255, 255, 255))

        # player movement and drawing
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a]:
            move_player("left")
        if pressed[pygame.K_d]:
            move_player("right")

        draw_player()
        screen.blit(scaledPlaceholder, placeholder)

        # updating HUD values
        playerHealth = checkPlayerCollision(playerHealth)
        if playerHealth == 100:
            health = retro.render("Health: "+str(playerHealth)+"%", False, (0, 255, 0))
        elif playerHealth == 66:
            health = retro.render("Health: "+str(playerHealth)+"%", False, (255, 255, 0))
        else:
            health = retro.render("Health: "+str(playerHealth)+"%", False, (255, 0, 0))

        playerScore = checkEnemyCollision(playerScore)
        score = retro.render("Score: "+str(playerScore)+"", False, (R, G, B))
        R, G, B = rainbowLoop(R, G, B, 8)

        if doritoBreaches <= 2:
            breaches = retro.render("Doritos breached: "+str(doritoBreaches)+"", False, (0, 255, 0))
        elif doritoBreaches <= 4:
            breaches = retro.render("Doritos breached: "+str(doritoBreaches)+"", False, (255, 255, 0))
        elif doritoBreaches <= 6:
            breaches = retro.render("Doritos breached: "+str(doritoBreaches)+"", False, (255, 165, 0))
        else:
            breaches = retro.render("Doritos breached: "+str(doritoBreaches)+"", False, (255, 0, 0))

        # Lose conditions
        if playerHealth <= 0:
            runningGame = False
            gameOver = True
        if doritoBreaches >= 8:
            runningGame = False
            gameOver = True

        # updating and drawing the bullets
        i = 0
        for i in range(len(bullets)):
            if bullets[i].check:
                update_bullet(i)

        for i in range(len(bullets)):
            screen.blit(bullets[i]._image, bullets[i]._rect)

        # updating and drawing the enemies
        rand = random.randrange(0, 10)
        if rand == 1: 
            draw_enemies()

        for i in range(len(enemies)):
            if enemies[i].check():
                update_enemy(i)

        for i in range(len(enemies)):
            screen.blit(enemies[i]._image, enemies[i]._rect)

        for i in range(len(enemies)):
            if enemies[i].get_y() >= 720 and enemies[i].get_y() < 800:
                doritoBreaches += 1
                enemies[i].y(-50)
                enemies[i].x(random.randrange(1, 1231))

        # drawing the HUD
        screen.blit(ammo, (1, 1))
        screen.blit(health, (1, 25))
        screen.blit(score, (1, 50))
        screen.blit(breaches, (1, 75))

        pygame.display.update()
        clock.tick(60)
    while gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = False
                runningLoop = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                typing = True
            elif event.type == pygame.KEYDOWN and typing:
                if event.key == pygame.K_RETURN:
                    if not hasSubmitted and len(username) > 0:
                        typing = False
                        requests.post("http://127.0.0.1:5000/post/"+username+"/"+str(playerScore)+"")
                        hasSubmitted = True
                if event.key == pygame.K_ESCAPE:
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    if len(username) < 21:
                        username += event.unicode
            elif event.type == pygame.KEYDOWN and not typing:
                if event.key == pygame.K_r:
                    playerHealth = 100
                    playerScore = 0
                    magIndex = 5
                    ammo = retro.render("Ammo: 5/5", False, (255, 255, 255))
                    doritoBreaches = 0
                    enemies.clear()
                    create_enemies(enemies)
                    gameOver = False
                    runningGame = True
                    hasSubmitted = False
                    username = ""

        finalScore = retro.render("Final Score: "+str(playerScore)+"", False, (0, 0, 0))
        nameText = retro.render(username, False, (0, 0, 0))
        screen.fill((255, 0, 0))
        screen.blit(gameOverText, (300, 100))
        if playerHealth <= 0:
            screen.blit(healthEnd, (450, 250))
        else:
            screen.blit(breachedEnd, (300, 250))
        screen.blit(finalScore, (460, 300))
        screen.blit(restartText, (460, 350))
        screen.blit(submissionText, (170, 400))
        if hasSubmitted:
            screen.blit(submitted, (460, 475))
        else:
            screen.blit(nameText, (460, 475))
        pygame.display.update()

pygame.quit()
quit()