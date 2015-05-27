#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import sys
import time
import pygame
import Image
from pygame.locals import * 
# Constantes
WIDTH = 640
HEIGHT = 480 
SPEED = 0.3
BORDES = 3
# Clases
# ---------------------------------------------------------------------
class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("./Imagenes/pacman3.png", True)
        self.rect = self.image.get_rect()
        print self.rect.width,self.rect.width
        self.rect.centerx = BORDES + self.rect.width/2
        self.rect.centery = HEIGHT - self.rect.height/2 - BORDES
        self.speed = [0, 0]
    def actualizar(self, time):
        self.rect.centerx += self.speed[0] * time
        self.rect.centery += self.speed[1] * time
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed[1] = -self.speed[1]
            self.rect.centery += self.speed[1] * time
    def mover(self, time, keys):
        if self.rect.top >= 0:
            if keys[K_UP]:
                self.speed[1] = -SPEED
                self.speed[0] = 0
        if self.rect.bottom <= HEIGHT:
            if keys[K_DOWN]:
                self.speed[1] = SPEED
                self.speed[0] = 0
        if self.rect.left >= 0:
            if keys[K_LEFT]:
                self.speed[0] = -SPEED
                self.speed[1] = 0
        if self.rect.right <= WIDTH:
            if keys[K_RIGHT]:
                self.speed[0] = SPEED
                self.speed[1] = 0
        if self.speed[0] > 0 and self.rect.right < WIDTH - BORDES or self.speed[0] < 0 and self.rect.left >= 0 + BORDES:
            self.rect.centerx += self.speed[0] * time
        if self.speed[1] < 0 and self.rect.top >= 0 + BORDES or self.speed[1] > 0 and self.rect.bottom < HEIGHT - BORDES:
            self.rect.centery += self.speed[1] * time
# ---------------------------------------------------------------------
 
# Funciones
# ---------------------------------------------------------------------
def load_image(filename, transparent=False):
    try: image = pygame.image.load(filename)
    except pygame.error, message:
        raise SystemExit, message
    image = image.convert()
    if transparent:
        color = image.get_at((0,0))
        image.set_colorkey(color, RLEACCEL)
    return image
# ---------------------------------------------------------------------

#----------------------------------------------------------------------
def main():
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Prueba de ventana")
    pacman = Pacman()
    keys = pygame.key.get_pressed()
    clock = pygame.time.Clock()
    while True:
        keys = pygame.key.get_pressed()
        time = clock.tick(60)
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                pygame.QUIT()
                sys.exit()
        screen.fill((0,0,0))
        #pacman.actualizar(time)
        pacman.mover(time,keys)
        screen.blit(pacman.image, pacman.rect)

        pygame.display.update()
    return 0
#---------------------------------------------------------------------------------------------
if __name__ == '__main__':
    pygame.init()
    main()
