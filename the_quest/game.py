from the_quest import WIDTH, HEIGHT, FPS
from the_quest.escenas import Portada, Game, Portada2, Ranking1,Ranking
import pygame

pygame.init()

class Quest():
    def __init__(self):
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.escenas = [Portada(screen),Portada2(screen), Game(screen),Ranking1(screen),Ranking(screen)]
        self.escena_activa = 0

    def start(self):
        while True:
            la_escena = self.escenas[self.escena_activa]
            la_escena.reset()
            la_escena.bucle_principal()

            self.escena_activa = (self.escena_activa + 1 ) % len(self.escenas)