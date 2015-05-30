#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import sys
import glob
import time
import pygame
import random
#import Image
from pygame.locals import * 
# Constantes
WIDTH = 640
HEIGHT = 480 
SPEED = 0.3
BORDES = 3
activado = 0
screen = pygame.display.set_mode((WIDTH,HEIGHT))
# Clases
# ---------------------------------------------------------------------

class Galleta(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("./Imagenes/cookie.png", True)
        self.rect = self.image.get_rect()
        #print self.rect.width,self.rect.width
        self.rect.centerx = WIDTH/2
        self.rect.centery = HEIGHT/2  

# ----------------------------------------------------------------------      
class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ani = glob.glob("./Imagenes/moviendose/pac*.png")
        self.ani.sort()
        self.ani_pos = 0
        self.ani_max = len(self.ani) - 1
        self.image = load_image(self.ani[0], True)
        self.rect = self.image.get_rect()
        print self.rect.width,self.rect.height
        self.rect.centerx = BORDES + self.rect.width/2
        self.rect.centery = HEIGHT - self.rect.height/2 - BORDES
        self.speed = [0, 0]
        self.actualizarMovimiento(0)
        
    def actualizar(self, time):
        self.rect.centerx += self.speed[0] * time
        self.rect.centery += self.speed[1] * time
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed[1] = -self.speed[1]
            self.rect.centery += self.speed[1] * time
            
    def actualizarMovimiento(self,pos):
        if pos != 0:
            if self.speed != [0,0]:
                self.image = load_image(self.ani[self.ani_pos],True)
                if self.ani_pos == self.ani_max:
                    self.ani_pos=0
                else:
                    self.ani_pos+=1
                    
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
    pos = 0
    activado = 0
    pygame.display.set_caption("Prueba de ventana")
    pacman = Pacman()
    galleta = Galleta()
    pygame.mixer.init()
    pygame.mixer.music.load("./Sound/pacman_chomp.wav")
    keys = pygame.key.get_pressed()
    clock = pygame.time.Clock()
    while True:
        keys = pygame.key.get_pressed()
        time = clock.tick(60)
        screen.fill((0,0,0))
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit()
        if keys[K_UP] or keys[K_DOWN] or keys[K_LEFT] or keys[K_RIGHT] and activado == 0:
            pygame.mixer.music.play(-1)
            activado = 1
            pos = 1
        pacman.mover(time,keys)
        pacman.actualizarMovimiento(pos)
        screen.blit(galleta.image, galleta.rect)
        screen.blit(pacman.image, pacman.rect)
        pygame.display.update()
    return 0
#---------------------------------------------------------------------------------------------
if __name__ == '__main__':
    pygame.init()
    main()
