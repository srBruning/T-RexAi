
import util
import values as  vl
import pygame
from event_watcher import EventWatcher

class Dino(EventWatcher):
    def __init__(self, context,sizex=-1,sizey=-1, position=15):
        self.context = context
        self.images,self.rect = util.load_sprite_sheet(
            'dino.png',5,1,sizex,sizey,-1, True)
        self.images1,self.rect1 = util.load_sprite_sheet( 
            'dino_ducking.png',2,1,59,sizey,-1)
        self.rect.bottom = int(0.98*context.height)
        self.rect.left = context.width/position
        self.image = self.images[0]
        self.index = 0
        self.counter = 0
        self.score = 0
        self.isJumping = False
        self.isDead = False
        self.isDucking = False
        self.isBlinking = False
        self.movement = [0,0]
        self.jumpSpeed = 11.5

        self.stand_pos_width = self.rect.width
        self.duck_pos_width = self.rect1.width

    def set_color(self, newColor):
        util.replaceColorSprints( self.images, (34, 91, 133), newColor)
        util.replaceColorSprints( self.images1, (34, 91, 133), newColor)

    def draw(self):
        self.context.screen.blit(self.image,self.rect)

    def checkbounds(self):
        if self.rect.bottom > int(0.98*self.context.height):
            self.rect.bottom = int(0.98*self.context.height)
            self.isJumping = False

    def update(self):
        pygame = self.context.pygame
        if self.isJumping:
            self.movement[1] = self.movement[1] + vl.gravity

        if self.isJumping:
            self.index = 0
        elif self.isBlinking:
            if self.index == 0:
                if self.counter % 400 == 399:
                    self.index = (self.index + 1)%2
            else:
                if self.counter % 20 == 19:
                    self.index = (self.index + 1)%2

        elif self.isDucking:
            if self.counter % 5 == 0:
                self.index = (self.index + 1)%2
        else:
            if self.counter % 5 == 0:
                self.index = (self.index + 1)%2 + 2

        if self.isDead:
           self.index = 4

        if not self.isDucking:
            self.image = self.images[self.index]
            self.rect.width = self.stand_pos_width
        else:
            self.image = self.images1[(self.index)%2]
            self.rect.width = self.duck_pos_width

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

        if not self.isDead and self.counter % 7 == 6 and self.isBlinking == False:
            self.score += 1
            if self.score % 100 == 0 and self.score != 0:
                if pygame.mixer.get_init() != None:
                    self.context.res().checkPoint_sound.play()

        self.counter = (self.counter + 1)

    def jump(self):
        if self.rect.bottom == int(0.98* self.context.height):
            self.isJumping = True
            if pygame.mixer.get_init() != None:
                self.context.res().jump_sound.play()
            self.movement[1] = -1*self.jumpSpeed

    def duck_down(self):
        
        if not (self.isDead):
            self.isDucking = True
            if(self.isJumping):
                self.movement[1] = self.movement[1] + vl.gravity

    def get_up(self):
        self.isDucking = False    

    def notifyEvent(self, event):
        # for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.jump()

            if event.key == pygame.K_DOWN:
                self.duck_down()

            if event.key == pygame.K_UP:
                self.jump()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                self.get_up()

    def status(self):
        # self.context
        pass
