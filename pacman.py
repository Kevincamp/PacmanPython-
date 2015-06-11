#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import sys
import glob
import time
import pygame
import random
#import Image
from pared import Pared
from pygame.locals import * 
# Constantes
WIDTH = 640
HEIGHT = 640 
DIMMAZE = 20
SPEED = 0.3
DIMENSION = 32
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
        self.generarSalida(laberinto,self.mazeHeight,self.mazeWidth)
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
                    elif(i==height-2):
                        if(laberinto[i-1][j]==1 and laberinto[i][j-1]==1):
                            laberinto[i][j]=1
                            
                            
                #abajoconMarco    
                elif(i == height-2 and j>1 and j<width-2):
                    if(laberinto[i][j]==0 and laberinto[i][j-1]==0 and laberinto[i-1][j-1]==0 and laberinto[i-1][j]==0 and laberinto[i-1][j+1]==0 and laberinto[i][j+1]==0):
                        laberinto[i][j] = 1
                    elif(laberinto[i][j]==0 and j!=2 and j!=width-2 and laberinto[i-1][j]==0 and laberinto[i][j-1]==0 and laberinto[i-1][j-1]==0):
                        laberinto[i][j] = 1
                else:
                    if(laberinto[i][j]==0 and laberinto[i][j-1]==0 and laberinto[i-1][j-1]==0 and laberinto[i-1][j]==0 and laberinto[i-1][j+1]==0 and laberinto[i][j+1]==0):
                        laberinto[i][j] = 1
                        if(i!=height-3):
                            self.ponerMuro(laberinto,i,j,"centro")
                        else:
                            self.ponerMuro(laberinto,i,j,"centropenultimo")
                    elif(laberinto[i][j]==0 and laberinto[i][j-1]==0 and laberinto[i-1][j-1]==0 and laberinto[i-1][j]==0):
                        if(i==height-3 and j==width-3):
                            laberinto[i][j] = 0
                        else:
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
        elif(estado=="centropenultimo"):
            pickR = random.randint(0,1)
            if(pickR==1):
                if(self.espaciosBlancoMuro(laberinto,i,j+1)):
                    laberinto[i][j+1] = 1
            
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
    
    def generarSalida(self, laberinto, height, width):
        murosSalidaUP = list()
        murosSalidaLEFT = list()
        murosSalidaRIGHT = list()
        murosSalidaDOWN = list()
        for j in range (0,width):
            if(laberinto[1][j]==0):
                murosSalidaUP.append(j)
            elif(laberinto[height-2][j]==0):
                murosSalidaDOWN.append(j)
        for i in range (0,height):
            if(laberinto[i][1]==0):
                murosSalidaLEFT.append(i)
            elif(laberinto[i][width-2]==0):
                murosSalidaRIGHT.append(i)
                
        selectorLista = random.randint(1,4)        
        
        if(selectorLista == 1):
            if(len(murosSalidaUP)!=0):
                muroSalida = random.choice(murosSalidaUP)
                laberinto[0][muroSalida] = 0
        elif(selectorLista == 2):
            if(len(murosSalidaDOWN)!=0):
                muroSalida = random.choice(murosSalidaDOWN)
                laberinto[height-1][muroSalida] = 0
        elif(selectorLista == 3):
            if(len(murosSalidaLEFT)!=0):
                muroSalida = random.choice(murosSalidaLEFT)
                laberinto[muroSalida][0] = 0
        else:
            if(len(murosSalidaRIGHT)!=0):
                muroSalida = random.choice(murosSalidaRIGHT)
                laberinto[muroSalida][width-1] = 0
        return 0
    
        
        
# ---------------------------------------------------------------------
class Galleta(pygame.sprite.Sprite):
    def __init__(self,x,y, nombre):
        pygame.sprite.Sprite.__init__(self)
        self.nombre = nombre
        self.image = load_image("./Imagenes/cookie.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = x + 16
        self.rect.centery = y + 16
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
        self.rect.topleft = (32,HEIGHT-66)
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
    countgalleta = 1
    countmuro = 1
    activado = 0
    Pared_x=0
    Pared_y=0
    lista = []
    maze = Laberinto(DIMMAZE,DIMMAZE)
    sprites = pygame.sprite.RenderUpdates()
    pygame.display.set_caption("Prueba Pacman")
    background = screen.copy()
    laberinto  = maze.getMaze()
    pacman = Pacman()
    galleta = Galleta(0,0)
    sprites.add(pacman)
    pygame.mixer.init()
    pygame.mixer.music.load("./Sound/pacman_chomp.wav")
    keys = pygame.key.get_pressed()
    clock = pygame.time.Clock()	
    for i in range(DIMMAZE):
            for j in range(DIMMAZE):
                if(laberinto[i][j] == 1):
                    sprites.add(Pared((0,0,255),(Pared_x,Pared_y),(DIMENSION,DIMENSION),("muro"+str(countmuro))))
                    countmuro += 1
                    Pared_x+=DIMENSION
                else:
                    sprites.add(Galleta(Pared_x,Pared_y,("galleta"+str(countgalleta))))
                    countgalleta += 1
                    Pared_x+=DIMENSION
            Pared_x=0
            Pared_y+=DIMENSION 

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
        sprites.update ()
        sprites.clear (screen, background)
        pygame.display.update (sprites.draw (screen))
        #screen.blit(galleta.image, galleta.rect)
        #screen.blit(pacman.image, pacman.rect)
        pygame.display.update()
    return 0
#---------------------------------------------------------------------------------------------
if __name__ == '__main__':
    pygame.init()
    main()