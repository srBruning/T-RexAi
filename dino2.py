
import util
import values as  vl
import pygame
from event_watcher import EventWatcher
from dino import Dino
from ai.neuronio import RedeNeural
import logging
logging.basicConfig(filename='app.log', filemode='w', format='%(message)s')


class Dino2(Dino):
    def __init__(self, context,sizex=-1,sizey=-1, position=15, redeNeural=None ):
        Dino.__init__(self,  context,sizex,sizey, position)
        if(redeNeural!=None):
            self.redeNeural = redeNeural
        else:
            self.redeNeural = RedeNeural()
    
    def notifyEvent(self, event):
        pass

    def status(self):
        ob = self.procurarProximoObstaculo()
        if ob ==None:
            return

        entrada = []
        entrada.append(ob.rect.x - self.rect.x)# DistanciaProximoObstaculo(Dinossauros[i].X);            
        entrada.append(ob.rect.width)# LarguraProximoObstaculo(Dinossauros[i].X);              
        entrada.append(ob.rect.height)# AlturaProximoObstaculo(Dinossauros[i].X);               
        entrada.append(ob.rect.y)# ComprimentoProximoObstaculo(Dinossauros[i].X);
        entrada.append(self.context.speed)# fabs(VELOCIDADE);
        entrada.append(self.rect.y)# Dinossauros[i].Y;  
        logging.error(entrada)
      
        self.redeNeural.setEntrada(entrada)
        self.redeNeural.calcularSaida()
        saida = self.redeNeural.getSaida()
        if saida[0] != 0:
            self.jump()
        if saida[1] != 0:
            self.duck_down()
        if saida[2] != 0:
            self.get_up()

    def procurarProximoObstaculo(self):
        menor = None
        
        for l in self.context.last_obstacle:
            if ( menor==None or  l.rect.x < menor.rect.x):
                menor = l
        return menor

   