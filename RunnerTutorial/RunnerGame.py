'''

@Author: Ratman457
Following tutorial: https://www.youtube.com/watch?v=AY9MnQ4x3zk&t=155s
@authorOfTutorial: Clear Code
@authorGithub: https://github.com/clear-code-projects/UltimatePygameIntro

Written in Python 3

Started: Mar 10 2023
Finished Mar 11 2023

Added extra frame to fly animation
Edited and added coin images + collision + motion + extra score
@authorOfCoins: https://laredgames.itch.io/gems-coins-free

'''

import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self): 
        super().__init__()
        
        playerWalk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        playerWalk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.playerWalk = [playerWalk1, playerWalk2]
        self.playerIndex = 0
        self.playerJump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
        
        self.image = self.playerWalk[self.playerIndex]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0
        self.jumpSound = pygame.mixer.Sound('audio/audio_jump.mp3')
        self.jumpSound.set_volume(0.1)
    
    def playerInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.jumpSound.play()
            self.gravity = -20
    
    def applyGrav(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300 :
            self.rect.bottom = 300
    
    def animationState(self):
        if self.rect.bottom < 300:
            self.image = self.playerJump
        else:
            self.playerIndex += 0.1
            if self.playerIndex >= len(self.playerWalk): self.playerIndex = 0
            self.image = self.playerWalk[int(self.playerIndex)]
    
    def update(self):
        self.playerInput()
        self.applyGrav()
        self.animationState()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, oType):
        super().__init__()
        
        if oType == 'fly':
            flyFrame1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            flyFrame2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            flyFrame3 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            self.frames = [flyFrame1, flyFrame2, flyFrame3]
            self.animationSpeed = 0.2
            self.moveSpeed = 6
            y_pos = 210
        else:
            snailFrame1 = pygame.image.load('graphics/Snail/snail1.png').convert_alpha() # .convert_alpha respects alpha in the image (invisible pixels)
            snailFrame2 = pygame.image.load('graphics/Snail/snail2.png').convert_alpha()
            self.frames = [snailFrame1, snailFrame2]
            self.animationSpeed = 0.1
            self.moveSpeed = 6
            y_pos = 300
        
        self.animationIndex = 0
        self.image = self.frames[self.animationIndex]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))
    
    def animationState(self):
        self.animationIndex += self.animationSpeed
        if self.animationIndex >= len(self.frames): self.animationIndex = 0
        self.image = self.frames[int(self.animationIndex)]
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
    
    def update(self):
        self.animationState()
        self.rect.x -= self.moveSpeed
        self.destroy()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        coinFrame1 = pygame.image.load('graphics/coin/coin1.png').convert_alpha()
        coinFrame2 = pygame.image.load('graphics/coin/coin2.png').convert_alpha()
        coinFrame3 = pygame.image.load('graphics/coin/coin3.png').convert_alpha()
        coinFrame4 = pygame.image.load('graphics/coin/coin4.png').convert_alpha()
        coinFrame5 = pygame.image.load('graphics/coin/coin5.png').convert_alpha()
        self.frames = [coinFrame1, coinFrame2, coinFrame3, coinFrame4, coinFrame5]
        self.animationSpeed = 0.1
        self.moveSpeed = 6
        
        self.maxYPos = 150
        self.minYPos = 250
        self.yMove = -2
        
        self.animationIndex = 0
        self.image = self.frames[self.animationIndex]
        self.rect = self.image.get_rect(center = (randint(600, 700), randint(150, 250)))
    
    def animationState(self):
        self.animationIndex += self.animationSpeed
        if self.animationIndex >= len(self.frames): self.animationIndex = 0
        self.image = self.frames[int(self.animationIndex)]
        
    def coinMove(self):
        self.rect.y += self.yMove
        if self.rect.top <= 150: self.yMove = 2
        if self.rect.top >= 250: self.yMove = -2

    def destroy(self):
            if self.rect.x <= -100:
                self.kill()

    def update(self):
        self.animationState()
        self.rect.x -= self.moveSpeed
        self.destroy()
        self.coinMove()

def displayScore(coins):
    curTime = int((pygame.time.get_ticks() - startTime) / 1000) + (int(coins) * 10)
    scoreSurface = testFont.render(f'Score: {curTime}', False, (64, 64, 64))
    scoreRectangle = scoreSurface.get_rect(center = (400, 50))
    screen.blit(scoreSurface, scoreRectangle)
    return curTime

def obstacleCollisions():
    if pygame.sprite.spritecollide(player.sprite, obstacleGroup, False):
        obstacleGroup.empty()
        coin.empty()
        return False
    else: return True

def coinCollisions():
    if pygame.sprite.spritecollide(player.sprite, coin, True):
        coin.empty()
        return True
    else: return False

# Pre-Gameloop setup
pygame.init() # Actually starts the pygame process
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Pixel Runner') # Sets the window title
clock = pygame.time.Clock()
testFont = pygame.font.Font('font/Pixeltype.ttf', 50)
gameActive = False # Starts the game in the 'game over menu'
startTime = 0
score = 0
coinAmmount = 0

# Music
bgMusic = pygame.mixer.Sound('audio/music.wav')
bgMusic.set_volume(0.1)
bgMusic.play(loops = -1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

coin = pygame.sprite.GroupSingle()
coin.add(Coin())

obstacleGroup = pygame.sprite.Group()

# Create surfaces (Except for the main screen)
skySurface = pygame.image.load('graphics/Sky.png').convert() # .convert makes the images easier for pygame to work with
groundSurface = pygame.image.load('graphics/ground.png').convert()

# Intro screen
playerStand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
playerStand = pygame.transform.rotozoom(playerStand, 0, 2)
playerStandRect = playerStand.get_rect(center = (400, 200))

gameName = testFont.render('Pixel Runner', False, (111, 196, 169))
gameNameRectangle = gameName.get_rect(center = (400, 50))

endTitleSurface = testFont.render('Press SPACEBAR to start running', False, (111, 196, 169))
endTitleRectangle = endTitleSurface.get_rect(center = (400, 350))

# Timers
obsticeleTimer = pygame.USEREVENT + 1
pygame.time.set_timer(obsticeleTimer, 1100)

coinTimer = pygame.USEREVENT + 2
pygame.time.set_timer(coinTimer, 5000)

# Gameloop
while True:
    for event in pygame.event.get(): # Looks for any events that occur
        if event.type == pygame.QUIT: # If the user closes the window the code actually stops
            pygame.quit()
            exit() # Stops the code from trying to update the display when we have un-initilised pygame
        
        if gameActive:
            
            # Add obstacles to the screen            
            if event.type == obsticeleTimer: 
                obstacleGroup.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
            
            # add coins to the screen (coins are a Groupsingle type so only one will ever be present)
            if event.type == coinTimer:
                coin.add(Coin())
                
        else: # Waits for spacebar to start again
            startTime = pygame.time.get_ticks()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameActive = True
        
    if gameActive:
        
        # Place static surfaces on the screen
        screen.blit(skySurface,(0,0))
        screen.blit(groundSurface,(0,300))
        score = displayScore(coinAmmount)
        
        # Place sprites and update them
        player.draw(screen)
        player.update()
        
        obstacleGroup.draw(screen)
        obstacleGroup.update()
        
        coin.draw(screen)
        coin.update()
        
        # Check for coin collision
        if coinCollisions():
            coinAmmount += 1
        
        # Check for obstacle collision
        gameActive = obstacleCollisions()
        
    else:
        
        # Reset variables
        coinAmmount = 0
        playerGrav = 0
        
        # Place end screen stuff
        screen.fill((94, 129, 162))
        screen.blit(playerStand, playerStandRect)
        screen.blit(gameName, gameNameRectangle)
        
        endScoreSurface = testFont.render(f'Your Score: {score}', False, (111, 196, 169))
        endScoreRectangle = endScoreSurface.get_rect(center = (400, 350))
        
        if score == 0:
            screen.blit(endTitleSurface, endTitleRectangle)
        else:
            screen.blit(endScoreSurface, endScoreRectangle)
        
    pygame.display.update() # This actually keeps the display on screen
    clock.tick(60) # Sets the maximum frame rate and is tied to game speed
    
