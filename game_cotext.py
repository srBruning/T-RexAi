from res import Res

class GameContext:
    def __init__(self, pygame, screen, width, height, speed):
        self.pygame = pygame
        self.width = width
        self.height = height
        self._res = None
        self.screen = screen
        self.speed = speed
        self.gameOver = False
        self.gameQuit = False
   
    def res(self):
        if self._res == None :
            self._res = Res(self)
        return self._res