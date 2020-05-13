import values as vl

class Res:
    def __init__(self, context):
        pygame = context.pygame
        self.jump_sound = pygame.mixer.Sound(vl.res_path
            +'/jump.wav')
        self.die_sound = pygame.mixer.Sound(vl.res_path
            +'/die.wav')
        self.checkPoint_sound = pygame.mixer.Sound(vl.res_path
            +'/checkPoint.wav')