import os
import pygame
import time
import random
import pickle


pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (150,220,30)
blue = (0,0,255)

display_width = 780
display_height  = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('snakame')

# loading images
bg = pygame.image.load('background.png') 

icon = pygame.image.load('apple.png')
pygame.display.set_icon(icon)


img = pygame.image.load('snake.png')
introimg = pygame.image.load('snakame.png')
appleimg = pygame.image.load('apple.png')
bananaimg = pygame.image.load('banana.png')


clock = pygame.time.Clock()

AppleThickness = 32
BananaThickness = 60
block_size = 30
FPS = 10

direction = "right"

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)
exlargefont = pygame.font.SysFont("comicsansms", 150)


def score(score):
    text = smallfont.render("Score: "+str(score), True, red)
    gameDisplay.blit(text, [0,0])

def timer(b):
    text = smallfont.render("Score: "+str(b), True, red)
    gameDisplay.blit(text, [300,0])

def randAppleGen():
    randAppleX = round(random.randrange(0, display_width-AppleThickness))
    randAppleY = round(random.randrange(0, display_height-AppleThickness))

    return randAppleX,randAppleY



def game_intro():

    intro = True

##    score_file=open("score.txt","r")
##    score_value=score_file.read()
##    score_file.close()

    scores = open("score.dat", "r")
    h_c = pickle.load(scores)
    h=(h_c[0][1]**29)%91
    scores.close()
    
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.blit(introimg,(0,0))
        text = smallfont.render("High Score: "+str(h), True, white)
        gameDisplay.blit(text, [600,0])
   
##        gameDisplay.fill(green)
##
##        message_to_screen("High Score: " + str(h),
##                          blue,
##                          -280,
##                          "small")
##        
##        message_to_screen("Welcome to Snakame",
##                          red,
##                          -100,
##                          "large")
##        message_to_screen("The more apples you eat, the longer you get",
##                          black,
##                          10)
##
##        message_to_screen("Press C to play or Q to quit.",
##                          black,
##                          180)
    
        pygame.display.update()
        clock.tick(15)

    


def snake(block_size, snakelist):

    if direction == "right":
        head = img
        
    if direction == "left":
        head = pygame.transform.rotate(img, 180)

    if direction == "up":
        head = pygame.transform.rotate(img, 90)

    if direction == "down":
        head = pygame.transform.rotate(img, 270)
    
    gameDisplay.blit(head, (snakelist[-1][0], snakelist[-1][1]))
    
    for i in range(0,len(snakelist)-1):
        XnY=snakelist[i]
        if 10+i < block_size/2:
            pygame.draw.circle(gameDisplay, black, (XnY[0]+16,XnY[1]+16),10+i,0)
        else:
            pygame.draw.circle(gameDisplay, black, (XnY[0]+16,XnY[1]+16),block_size/2,0)

    
def text_objects(text,color,size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    elif size == "exlarge":
        textSurface = exlargefont.render(text, True, color)

    
    return textSurface, textSurface.get_rect()
    
    
def message_to_screen(msg,color, y_displace=0, size = "small"):
    textSurf, textRect = text_objects(msg,color, size)
    textRect.center = (display_width / 2), (display_height / 2)+y_displace
    gameDisplay.blit(textSurf, textRect)


def pause():
    paused=True

    scores = open("score.dat", "r")
    h_c = pickle.load(scores)
    h=(h_c[0][1]**29)%91
    scores.close()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_p:
                    pygame.mixer.music.load("pause.mp3")
                    pygame.mixer.music.play(0, 0.0)
                    paused=False
                    
##        gameDisplay.fill(white)
        message_to_screen("Paused",black,-50,"large")
        message_to_screen("High Score: " + str(h),
                          white,
                          50,
                          "small")
        message_to_screen("press P to continue & Q to quit.",
                      blue,
                      150,"medium")
        pygame.display.update()
        clock.tick(5)

                    
def gameLoop():
    global direction

    direction = 'right'
    gameExit = False
    gameOver = False

    lead_x = display_width/2
    lead_y = display_height/2

    lead_x_change = 30
    lead_y_change = 0

    r_direct = True
    l_direct = False
    u_direct = False
    d_direct = False

    bonus_control=False

    scr=0

    snakeList = []
    snakeLength = 4

##    bananaX = -1
##    bananaY = -1

    bonus_on = pygame.time.get_ticks()

    bonus=random.randrange(0,10)

    bananaX = random.randrange(0, display_width-BananaThickness)
    bananaY = random.randrange(0, display_height-BananaThickness)

    randAppleX,randAppleY = randAppleGen()

    pygame.mixer.music.load("start.wav")
    pygame.mixer.music.play(0, 0.0)
    
    while not gameExit:

        while gameOver == True:
##            gameDisplay.fill(white)
            
            scores = open("score.dat", "r")
            h_c = pickle.load(scores)
            h=(h_c[0][1]**29)%91
            scores.close()

            text = medfont.render("Score: "+str(scr), True, white)
            gameDisplay.blit(text, [300,250])

            message_to_screen("High Score: " + str(h),
                          white,
                          50,
                          "medium")
            
            message_to_screen("Game over",
                              red,
                              y_displace=-150,
                              size="exlarge")
            
            message_to_screen("Press C to play again or Q to quit",
                              blue,
                              150,
                              size="medium")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if r_direct == False:
                        l_direct = True
                        u_direct = False
                        d_direct = False
                        direction = "left"
                        lead_x_change = -block_size
                        lead_y_change = 0
                    else:
                        continue
                elif event.key == pygame.K_RIGHT:
                    if l_direct == False:
                        r_direct = True
                        u_direct = False
                        d_direct = False
                        direction = "right"
                        lead_x_change = block_size
                        lead_y_change = 0
                    else:
                        continue
                elif event.key == pygame.K_UP:
                    if d_direct == False:
                        r_direct = False
                        u_direct = True
                        l_direct = False
                        direction = "up"
                        lead_y_change = -block_size
                        lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    if u_direct == False:
                        d_direct = True
                        r_direct = False
                        l_direct = False
                        direction = "down"
                        lead_y_change = block_size
                        lead_x_change = 0
                elif event.key == pygame.K_p:
                    pygame.mixer.music.load("pause.mp3")
                    pygame.mixer.music.play(0, 0.0)
                    pause()

        if lead_x > display_width or lead_x  < 0 or lead_x + block_size > display_width or lead_x + block_size < 0 or lead_y + block_size > display_height or lead_y + block_size < 0 or lead_y  > display_height or lead_y < 0:
            gameOver = True
            pygame.mixer.music.load("gameover.wav")
            pygame.mixer.music.play(0, 0.0)
      

        lead_x += lead_x_change
        lead_y += lead_y_change
        
        gameDisplay.blit(bg,(0,0))

        gameDisplay.blit(appleimg, (randAppleX, randAppleY))
        
        
        if bonus ==6 or bonus ==9:
            bonus_control=True
            gameDisplay.blit(bananaimg, (bananaX, bananaY))
        else:
            bananaX=100
        
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True
                game_over_music = pygame.mixer.music.load("gameover.wav")
                pygame.mixer.music.play(0, 0.0)

        
        snake(block_size, snakeList)

        
        score(scr)

        

##        score_f=open("score.txt","r")
##        score_v=int(score_f.read())
##        score_f.close()

        scores = open("score.dat", "r")
        h_c = pickle.load(scores)
        h=int((h_c[0][1]**29)%91)
        scores.close()        

             
        if h < scr:
            h_c=(scr**5)%91 
            hiscore=[("h",h_c)]

            scores = open("score.dat", "w")
            pickle.dump(hiscore, scores)
            scores.close()

        
        pygame.display.update()


        

        if lead_x > randAppleX and lead_x < randAppleX + AppleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + AppleThickness:

            if lead_y > randAppleY and lead_y < randAppleY + AppleThickness or lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + AppleThickness:

                eat_music = pygame.mixer.music.load("eat.mp3")
                pygame.mixer.music.play(0, 0.0)
                
                randAppleX,randAppleY = randAppleGen()
                scr += 1
                snakeLength +=1
                bonus=random.randrange(0,10)
                bananaX = random.randrange(0, display_width-BananaThickness)
                bananaY = random.randrange(0, display_height-BananaThickness)
                
        if bonus_control == True:    
            if lead_x > bananaX and lead_x < bananaX + BananaThickness or lead_x + block_size > bananaX and lead_x + block_size < bananaX + BananaThickness:

                if lead_y > bananaY and lead_y < bananaY + BananaThickness or lead_y + block_size > bananaY and lead_y + block_size < bananaY + BananaThickness:

                    eat_music = pygame.mixer.music.load("eat.mp3")
                    pygame.mixer.music.play(0, 0.0)

                    bananaX = random.randrange(0, display_width-BananaThickness)
                    bananaY = random.randrange(0, display_height-BananaThickness)
                    bonus=random.randrange(0,10)
                    bonus_control = False
                    scr += 5
                    snakeLength +=1

            
             

        clock.tick(FPS)
        
        
        
    pygame.quit()
    quit()

game_intro()
gameLoop()
