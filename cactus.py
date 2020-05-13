import pygame
from util import load_sprite_sheet
import random

class Cactus(pygame.sprite.Sprite):
    def __init__(self,context,sizex=-1,sizey=-1):
        self.context = context
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images,self.rect = load_sprite_sheet( 'cacti-small.png',
            3,1,sizex,sizey,-1)
        self.rect.bottom = int(0.98*context.height)
        self.rect.left = context.width + self.rect.width
        self.image = self.images[random.randrange(0,3)]
        self.movement = [-1*context.speed,0]

    def draw(self):
        self.context.screen.blit(self.image,self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:
            self.kill()