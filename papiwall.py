import pygame
import random

pygame.init()
pygame.display.set_caption("PapiWall")

cloudPicture = pygame.image.load('cloudsmall.png')
smileys = [pygame.image.load('smiley.png'),pygame.image.load('smiley1.png'),pygame.image.load('smiley2.png'),pygame.image.load('smiley3.png'),pygame.image.load('smiley4.png'),pygame.image.load('smiley5.png'),pygame.image.load('smiley6.png'),pygame.image.load('smiley7.png'),pygame.image.load('smiley8.png'),pygame.image.load('smiley9.png'),pygame.image.load('smiley10.png'),pygame.image.load('smiley11.png')]
ballpicture = pygame.image.load('ball2.png')
boingsound = pygame.mixer.Sound('boing.wav')
failsound = pygame.mixer.Sound('fail.wav')


WIDTH = 600
HEIGHT = 500
BROWN = (90,45,0)
RED = (250,0,0)
BLUE = (20,161,255)
BLACK = (0,0,0)
LIGHTBROWN = (244,164,96)
BALLRADIUS = 35
WALLTHICKNESS = 15


screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Score:
    score = 0

    def countScore(self):
        self.score += 1

    def printScore(self, fontSize, color, width, height):
        font = pygame.font.Font('freesansbold.ttf', fontSize)
        textInfo = font.render('Score: ' + str(self.score), False, color)
        screen.blit(textInfo, (width, height))

class Cloud: 
    def __init__(self):
        self.x = random.randint(0, WIDTH//2)
        self.y = random.randint(0, HEIGHT//7)
        self.cloudSpeed = 2

    def show(self):
        screen.blit(cloudPicture, (self.x,self.y))

    def moveCloud(self):
        if self.x > WIDTH:
            self.x = -200
            self.y = random.randint(0, HEIGHT//5)
        self.x += self.cloudSpeed

class Ball:
    radius = BALLRADIUS
    isJumping = False
    jumpCount = 9
    slowJump = 0
    smileyCount = 11
    saveSmiley = 0
    angle = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    #falsch für collision • Rect.collidepoint(point) ? 
    def checkForCollusion(self, wall):
        if wall.getRect().collidepoint(self.x, self.y) or wall.getRect().collidepoint(self.x +self.radius , self.y) or wall.getRect().collidepoint(self.x-self.radius, self.y) or wall.getRect().collidepoint(self.x, self.y+self.radius) or wall.getRect().collidepoint(self.x, self.y-self.radius):
            return True
        return False

    def ballRoutine(self,wall):
        self.print(RED)


    def print(self,color):
        pygame.draw.circle(screen, color , (self.x, self.y), self.radius)
        #picture = pygame.transform.rotate(smileys[0], self.angle)
        #screen.blit(picture, (self.x-35,self.y-35))
        #rotatedBall = pygame.transform.rotate(ballpicture, self.angle)
        #screen.blit(rotatedBall, (self.x, self.y-50))
        if wallIsMoving:    
            self.angle += 15
        screen.blit(smileys[self.smileyCount], (self.x-20,self.y-25))
        if self.saveSmiley % 2 == 0 and wallIsMoving:
            self.smileyCount -= 1
        self.saveSmiley += 1
        if self.smileyCount < 0:
            self.smileyCount = 11


    def jump(self):
        keys = pygame.key.get_pressed()
        if not self.isJumping:
            if keys[pygame.K_SPACE]:
                boingsound.play()
                self.isJumping = True
        else: 
            if self.jumpCount >= -9:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                if self.slowJump % 2 == 0:
                    self.y -= self.jumpCount ** 2 * neg
                    self.jumpCount -= 1
                self.slowJump += 1
            else:
                self.isJumping = False
                self.jumpCount = 9


class Wall:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 6
        self.wallCount = 0

    def getRect(self):
        return pygame.Rect( (self.x,self.y-self.getHillHeight()), (WALLTHICKNESS,HEIGHT))

    def show(self): # y wert von boden dazurechnen
        pygame.draw.rect(screen, LIGHTBROWN, pygame.Rect( (self.x,self.y-self.getHillHeight()), (WALLTHICKNESS,HEIGHT)))

    def moveWall(self):
        if self.x > WIDTH+WALLTHICKNESS: #check if wall went out on the right
            self.x = 0
            self.y = random.randint(150, 400)
            self.wallCount += 1
        else:
            self.x += self.speed + int (self.wallCount ** 0.6)

    def getHillHeight(self):
        sinAlpha = 0.98988299397
        sinBeta =  0.14188607488

        #hypothenuse = self.x / sinAlpha

        return sinBeta * self.x 


ball = Ball (WIDTH//8*7, 312)
wall = Wall(0, 250)
cloud = Cloud()
score = Score()

wallIsMoving = True
failSoundNotPlayed = True

run = True
while run:

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.draw.rect(screen, BLUE, pygame.Rect( (0,0), (WIDTH,HEIGHT)))
    pygame.time.delay(30)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()  # Quit the game
            quit()


    cloud.show()
    cloud.moveCloud()
    wall.show()
    if ball.checkForCollusion(wall):
        wallIsMoving = False
    if wallIsMoving:
         wall.moveWall()
         ball.jump()
         score.countScore()
    else:
        if failSoundNotPlayed:
            failsound.play()
            failSoundNotPlayed = False
    score.printScore(24, BLACK, 0, 0)
    ball.ballRoutine(wall)
    pygame.draw.polygon(screen, BROWN, [[0, HEIGHT//9*8],[0,HEIGHT] ,[WIDTH, HEIGHT], [WIDTH, HEIGHT//3*2]])
    pygame.display.update()  

