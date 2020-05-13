from util import load_sprite_sheet, extractDigits
import values as vl

class Scoreboard():
    def __init__(self,context, x=-1,y=-1):
        self.context = context
        self.score = 0
        self.tempimages,self.temprect = load_sprite_sheet( 'numbers.png',12,1,11,int(11*6/5),-1)
        self.image = context.pygame.Surface((55,int(11*6/5)))
        self.rect = self.image.get_rect()
        if x == -1:
            self.rect.left = context.width*0.89
        else:
            self.rect.left = x
        if y == -1:
            self.rect.top = context.height*0.1
        else:
            self.rect.top = y

    def draw(self):
        self.context.screen.blit(self.image,self.rect)

    def update(self,score):
        score_digits = extractDigits(score)
        self.image.fill(vl.background_col)
        for s in score_digits:
            self.image.blit(self.tempimages[s],self.temprect)
            self.temprect.left += self.temprect.width
        self.temprect.left = 0