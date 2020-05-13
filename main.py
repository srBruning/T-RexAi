import os
import sys
import pygame
import random
import time
from game_cotext import GameContext
import  values as vl
from util import *
from dino import Dino
from dino2 import Dino2
from scoreboard import Scoreboard
from cloud import Cloud
from ground import Ground
from ptera import Ptera
from cactus import Cactus

pygame.mixer.pre_init(44100, -16, 2, 2048) # fix audio delay 
pygame.init()
width,height = vl.scr_size

high_score = 0
screen = pygame.display.set_mode(vl.scr_size)
context = GameContext(pygame, screen, width, height, 5)

clock = pygame.time.Clock()
pygame.display.set_caption(vl.caption)

def disp_gameOver_msg(retbutton_image,gameover_image):
    retbutton_rect = retbutton_image.get_rect()
    retbutton_rect.centerx = width / 2
    retbutton_rect.top = height*0.52

    gameover_rect = gameover_image.get_rect()
    gameover_rect.centerx = width / 2
    gameover_rect.centery = height*0.35

    screen.blit(retbutton_image, retbutton_rect)
    screen.blit(gameover_image, gameover_rect)

def introscreen():
    temp_dino = createDino()
    temp_dino.isBlinking = True
    gameStart = False

    callout,callout_rect = load_image( 'call_out.png',196,45,-1)
    callout_rect.left = width*0.05
    callout_rect.top = height*0.4

    temp_ground,temp_ground_rect = load_sprite_sheet( 'ground.png',15,1,-1,-1,-1)
    temp_ground_rect.left = width/20
    temp_ground_rect.bottom = height

    logo,logo_rect = load_image( 'logo.png',240,40,-1)
    logo_rect.centerx = width*0.6
    logo_rect.centery = height*0.6
    while not gameStart:
        if pygame.display.get_surface() == None:
            print("Couldn't load display surface")
            return True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        temp_dino.isJumping = True
                        temp_dino.isBlinking = False
                        temp_dino.movement[1] = -1*temp_dino.jumpSpeed

        temp_dino.update()

        if pygame.display.get_surface() != None:
            screen.fill(vl.background_col)
            screen.blit(temp_ground[0],temp_ground_rect)
            if temp_dino.isBlinking:
                screen.blit(logo,logo_rect)
                screen.blit(callout,callout_rect)
            temp_dino.draw()

            pygame.display.update()

        clock.tick(vl.FPS)
        if temp_dino.isJumping == False and temp_dino.isBlinking == False:
            gameStart = True

def criar_obstatuclos( counter, cacti,pteras, clouds ):
    last_obstacle = context.last_obstacle

    if len(clouds) < 5 and random.randrange(0,300) == 10:
        Cloud(context.width,random.randrange(height/5,height/2)) 

    for l in last_obstacle:
        if l.rect.right > context.width*0.7:
            return

    if len(cacti) < 2:
        r = 10
        if len(cacti)>0 :
            r = random.randrange(0,60)
            
        if r == 10:
            last_obstacle.add(Cactus(context,30,40))
            return
        elif r == 30:
            last_obstacle.add(Cactus(context,70,50))
            return
        

    if len(pteras) == 0 and random.randrange(0,100) == 10 and counter > 500:
        last_obstacle.add(Ptera(context, 46, 40))   

def verificar_colizoes(players, matrisObstatculos):
    for  obs in matrisObstatculos :
        for c in obs:
            c.movement[0] = -1*context.speed
            for playerDino in players:
                if pygame.sprite.collide_mask(playerDino,c):
                    playerDino.isDead = True
                    if pygame.mixer.get_init() != None:
                        context.res().die_sound.play()  

def capture_event(context,players):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            context.gameQuit = True
            context.gameOver = True
            break
        for player in players:
            player.notifyEvent(event)


def createDino(tipo=1):
    if tipo ==1:
        d = Dino2(context, 43,47, position=random.randint(10,25))
    else:
        d = Dino(context, 43,47, position=random.randint(10,25))
        d.set_color(random_color())
    return d

def gameplay():
    global high_score
    context.speed = 4
    context.gameOver = False
    context.gameQuit = False
    start_time = time.time()
    playersDino = [createDino() for i in range(50) ]
    playersDino.append(createDino(2) )
    print("--- %s seconds ---" % (time.time() - start_time))
    new_ground = Ground(context)
    scb = Scoreboard(context)
    highsc = Scoreboard(context,width*0.78)
    counter = 0

    cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    context.last_obstacle = pygame.sprite.Group()

    Cactus.containers = cacti
    Ptera.containers = pteras
    Cloud.containers = clouds

    retbutton_image,_ = load_image( 'replay_button.png',35,31,-1)
    gameover_image,_ = load_image( 'game_over.png',190,11,-1)

    temp_images,temp_rect = load_sprite_sheet( 'numbers.png',12,1,11,int(11*6/5),-1)
    HI_image = pygame.Surface((22,int(11*6/5)))
    HI_rect = HI_image.get_rect()
    HI_image.fill(vl.background_col)
    HI_image.blit(temp_images[10],temp_rect)
    temp_rect.left += temp_rect.width
    HI_image.blit(temp_images[11],temp_rect)
    HI_rect.top = height*0.1
    HI_rect.left = width*0.73

    while not context.gameQuit:
        current_score =0
        while not context.gameOver:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                context.gameQuit = True
                context.gameOver = True
            else:
                capture_event(context, playersDino)
            
            for player in playersDino:
                player.status()
            
            # print(len(context.last_obstacle))
            verificar_colizoes(playersDino, (cacti, pteras))

            criar_obstatuclos(counter, cacti, pteras, clouds)

            if len(playersDino) >0:
                current_score = playersDino[0].score
            newPlyers =[] 
            
            for player in playersDino:
                player.update()
                if(not player.isDead):
                    newPlyers.append(player)
            playersDino = newPlyers
            cacti.update()
            pteras.update()
            clouds.update()
            new_ground.update()

            scb.update(current_score)
            highsc.update(high_score)

            if pygame.display.get_surface() != None:
                screen.fill(vl.background_col)
                new_ground.draw()
                clouds.draw(screen)
                scb.draw()
                if high_score != 0:
                    highsc.draw()
                    screen.blit(HI_image,HI_rect)
                cacti.draw(screen)
                pteras.draw(screen)
                for player in playersDino:
                    player.draw()

                pygame.display.update()
            clock.tick(vl.FPS)

            if len(playersDino) ==0 :
                context.gameOver = True
                if current_score > high_score:
                    high_score = current_score

            if counter%700 == 599:
                context.speed += 1

            counter = (counter + 1)

        if context.gameQuit:
            break

        while context.gameOver:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                context.gameQuit = True
                context.gameOver = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        context.gameQuit = True
                        context.gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            context.gameQuit = True
                            context.gameOver = False

                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            context.gameOver = False
                            gameplay()
            highsc.update(high_score)
            if pygame.display.get_surface() != None:
                disp_gameOver_msg(retbutton_image,gameover_image)
                if high_score != 0:
                    highsc.draw()
                    screen.blit(HI_image,HI_rect)
                pygame.display.update()
            clock.tick(vl.FPS)

    pygame.quit()
    quit()

def main():
    isGameQuit = introscreen()
    if not isGameQuit:
        gameplay()

main()
