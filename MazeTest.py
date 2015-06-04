#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import sys
import random

# Constantes
WIDTH = 16
HEIGHT = 16
def generacionAleatoria(laberintoParteIZQ, height, width):
    for i in range(2,height-2):
        for j in range(2,width/2-2):
            if(laberintoParteIZQ[i-1][j-1]==0 and laberintoParteIZQ[i][j-1]==0 and laberintoParteIZQ[i-1][j] == 0 and laberintoParteIZQ[i+1][j-1] == 0 and laberintoParteIZQ[i+1][j] == 0):
                laberintoParteIZQ[i][j] = 1
                ponerMuro(laberintoParteIZQ,i,j,height,width)
    return laberintoParteIZQ

def ponerMuro(laberintoParteIZQ,i,j,height,width):
    pickDURL = random.randint(1,4)
    if(pickDURL == 1):
        if(espaciosBlancoMuro(laberintoParteIZQ,i+1,j,"DOWN")):
            laberintoParteIZQ[i+1][j] = 1
    elif(pickDURL == 2):
        if(espaciosBlancoMuro(laberintoParteIZQ,i,j+1,"RIGHT")):
            laberintoParteIZQ[i][j+1] = 1
    elif(pickDURL == 3):
        if(espaciosBlancoMuro(laberintoParteIZQ,i,j-1,"LEFT")):
            laberintoParteIZQ[i][j-1] = 1
    elif(pickDURL == 4):
        if(espaciosBlancoMuro(laberintoParteIZQ,i-1,j,"UP")):
            laberintoParteIZQ[i-1][j] = 1
    return 0

def marcoLaberinto(laberintoParteIZQ, height, width):
        for i in range(0,height):
            for j in range(0,width/2):
                if(i==0 or i==height-1):
                    laberintoParteIZQ[i][j] = 1
                elif(j==0):
                    laberintoParteIZQ[i][j] = 1
        return laberintoParteIZQ

def espaciosBlancoMuro(laberintoParteIZQ,i,j,direccion):
    if(direccion == "DOWN"):
        if(laberintoParteIZQ[i+1][j-1] == 0 and laberintoParteIZQ[i+1][j] == 0 and laberintoParteIZQ[i+1][j+1] == 0):
            return True
        else:
            return False
    elif(direccion == "LEFT"):
        if(laberintoParteIZQ[i-1][j-1] == 0 and laberintoParteIZQ[i][j-1] == 0 and laberintoParteIZQ[i+1][j-1] == 0):
            return True
        else:
            return False
    elif(direccion == "RIGHT"):
        if(laberintoParteIZQ[i-1][j+1] == 0 and laberintoParteIZQ[i][j+1] == 0 and laberintoParteIZQ[i+1][j+1] == 0):
            return True
        else:
            return False
    else:
        if(laberintoParteIZQ[i-1][j-1] == 0 and laberintoParteIZQ[i-1][j] == 0 and laberintoParteIZQ[i-1][j+1] == 0):
            return True
        else:
            return False
        
        
def printMatrix(testMatrix):
        for i, element in enumerate(testMatrix):
              print ' '.join(str(element))
              

def main():
    laberintoParteIZQ = [[0 for _ in range((WIDTH/2))] for _ in range((HEIGHT))]
    laberintoParteIZQ = marcoLaberinto(laberintoParteIZQ,HEIGHT,WIDTH)
    laberintoParteIZQ = generacionAleatoria(laberintoParteIZQ,HEIGHT,WIDTH)
    printMatrix(laberintoParteIZQ)
    
    
if __name__ == '__main__':
    main()