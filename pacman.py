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
class Laberinto():
    mazeWidth = 0
    mazeHeight = 0
    def __init__(self,width,height):
        self.mazeWidth = width
        self.mazeHeight = height
        
    def getMaze(self):
        laberinto = [[0 for _ in range((self.mazeWidth))] for _ in range((self.mazeHeight))]
        laberinto = self.marcoLaberinto(laberinto,self.mazeHeight,self.mazeWidth)
        laberinto = self.generacionAleatoria(laberinto,self.mazeHeight,self.mazeWidth)
        return laberinto
    
    def generacionAleatoria(self,laberinto, height, width):
        muroInitSize = random.randint(1,width/2)
        muroInitList = [0 for _ in range(muroInitSize)]
        muroPos = [2,4]
        for x in range (0,muroInitSize):
            if(x != 0):
                muroX = random.choice(muroPos)
                if(muroX+muroInitList[x-1] < width - 1):
                    muroInitList[x]=muroX
                    laberinto[1][muroX] = 1
            else:
                muroX = random.choice([1,2])
                muroInitList[x]=muroX
                laberinto[1][muroX] = 1
        for i in range(2,height-1):
            for j in range(1,width-1):
                #izquierdoconMarco
                if(j == 1):
                    if(laberinto[i][j] == 0 and laberinto[i-1][j] == 0 and laberinto[i-1][j+1] == 0 and laberinto[i][j+1] == 0):
                        laberinto[i][j] = 1
                #derechoconMarco
                elif(j == width-2):
                    if(laberinto[i][j]==0 and laberinto[i][j-1] == 0 and laberinto[i-1][j-1] == 0 and laberinto[i-1][j] == 0):
                        laberinto[i][j] = 1
                #abajoconMarco    
                elif(i == height-2 and j>1 and j<width-2):
                    if(laberinto[i][j]==0 and laberinto[i][j-1]==0 and laberinto[i-1][j-1]==0 and laberinto[i-1][j]==0 and laberinto[i-1][j+1]==0 and laberinto[i][j+1]==0):
                        laberinto[i][j] = 1
                        self.ponerMuro(laberinto,i,j,"abajo")
                else:
                    if(laberinto[i][j]==0 and laberinto[i][j-1]==0 and laberinto[i-1][j-1]==0 and laberinto[i-1][j]==0 and laberinto[i-1][j+1]==0 and laberinto[i][j+1]==0):
                        laberinto[i][j] = 1
                        self.ponerMuro(laberinto,i,j,"centro")
                    elif(laberinto[i][j]==0 and laberinto[i][j-1]==0 and laberinto[i-1][j-1]==0 and laberinto[i-1][j]==0):
                        laberinto[i][j] = 1
        return laberinto
    
    def ponerMuro(self,laberinto,i,j,estado):
        #pickDR{down,right,downright}
        if(estado == "centro"):
            pickDR = random.randint(1,3)
            if(pickDR == 1):
                laberinto[i+1][j] = 1
            elif(pickDR == 2):
                if(self.espaciosBlancoMuro(laberinto,i,j+1)):
                    laberinto[i][j+1] = 1
            elif(pickDR == 3):
                if(self.espaciosBlancoMuro(laberinto,i,j+1)):
                    laberinto[i][j-1] = 1
                    laberinto[i+1][j] = 1
            return 0
        elif(estado == "abajo"):
            pickDR = random.randint(0,1)
            if(pickDR == 1):
                if(self.espaciosBlancoMuro(laberinto,i,j+1)):
                    laberinto[i][j+1] = 1
            return 0
            
    def marcoLaberinto(self,laberinto, height, width):
        for i in range(0,height):
            for j in range(0,width):
                if(i==0 or i==height-1):
                    laberinto[i][j] = 1
                elif(j==0 or j==width-1):
                    laberinto[i][j] = 1
        return laberinto
    
    def espaciosBlancoMuro(self,laberinto,i,j):
        if(laberinto[i-1][j+1] == 0 and laberinto[i][j+1] == 0):
            return True
        else:
            return False
        
        
# ---------------------------------------------------------------------
class Galleta(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("./Imagenes/cookie.png", True)
        self.rect = self.image.get_rect()
        #print self.rect.width,self.rect.width
        self.rect.centerx = WIDTH/2
        self.rect.centery = HEIGHT/2  
    def render(self,collision):
        if (collision==True):
            print "llego"
            self.kill()
            self.image.fill((0,0,0))
            
        

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
            
    #def actualizarMovimiento(self,pos):
        #if pos != 0:
            #if self.speed != [0,0]:
                #pos_init = pos
                #self.ani_pos = pos
                #self.ani_max = pos + 8
                
                #self.image = load_image(self.ani[self.ani_pos], True)
                #print self.ani[self.ani_pos]
                #if self.ani_pos == self.ani_max:
                    #self.ani_pos=pos_init
                #else:
                    #self.ani_pos+= 1
                    
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
                
        #Para paredes de la ventana.
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
def printMatrix(testMatrix):
        print ' ',
        for i in range(len(testMatrix[1])):
              print i,
        print
        for i, element in enumerate(testMatrix):
              print i, ' '.join(str(element))
              
#----------------------------------------------------------------------
def main():
    pos = 0
    activado = 0
    pygame.display.set_caption("Prueba Pacman")
    pacman = Pacman()
    galleta = Galleta()
    pygame.mixer.init()
    pygame.mixer.music.load("./Sound/pacman_chomp.wav")
    keys = pygame.key.get_pressed()
    clock = pygame.time.Clock()
    #maze = Laberinto(WIDTH,HEIGHT)
    def comerGalleta(x1,y1,w1,h1,x2,y2,w2,h2):
        if (x2+w2>=x1>=x2 and y2+h2>=y1>=y2):
            return True    
        elif (x2+w2>=x1+w1>=x2 and y2+h2>=y1>=y2):
            return True
        elif (x2+w2>=x1>=x2 and y2+h2>=y1+h1>=y2):
            return True
        elif (x2+w2>=x1+w1>=x2 and y2+h2>=y1+h1>=y2):
            return True
        else:
            return False
        
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
            
        comiendoGalleta=comerGalleta(galleta.rect.x,galleta.rect.y,galleta.rect.width,galleta.rect.height,pacman.rect.x,pacman.rect.y,pacman.rect.width,pacman.rect.height)
        galleta.render(comiendoGalleta)
        pacman.actualizarMovimiento(pos)
        pacman.mover(time,keys)
        screen.blit(galleta.image, galleta.rect)
        screen.blit(pacman.image, pacman.rect)
        pygame.display.update()
    return 0
#---------------------------------------------------------------------------------------------
if __name__ == '__main__':
    pygame.init()
    main()