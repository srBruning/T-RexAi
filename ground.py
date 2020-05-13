from util import load_image
class Ground():
    def __init__(self,context, direction=-1):
        self.image,self.rect = load_image( 'ground.png',-1,-1,-1)
        self.image1,self.rect1 = load_image( 'ground.png',-1,-1,-1)
        self.rect.bottom = context.height
        self.rect1.bottom = context.height
        self.rect1.left = self.rect.right
        self.context = context
        self.direction = direction

    def draw(self):
        self.context.screen.blit(self.image,self.rect)
        self.context.screen.blit(self.image1,self.rect1)

    def update(self):
        aux = (self.direction * self.context.speed)
        self.rect.left += aux
        self.rect1.left += aux

        if self.rect.right < 0:
            self.rect.left = self.rect1.right

        if self.rect1.right < 0:
            self.rect1.left = self.rect.right