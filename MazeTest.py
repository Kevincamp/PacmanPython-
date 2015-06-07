#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import sys
import random

# Constantes
WIDTH = 12
HEIGHT = 12
def generacionAleatoria(laberinto, height, width):
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
                    ponerMuro(laberinto,i,j,"abajo")
            else:
                if(laberinto[i][j]==0 and laberinto[i][j-1]==0 and laberinto[i-1][j-1]==0 and laberinto[i-1][j]==0 and laberinto[i-1][j+1]==0 and laberinto[i][j+1]==0):
                    laberinto[i][j] = 1
                    ponerMuro(laberinto,i,j,"centro")
                elif(laberinto[i][j]==0 and laberinto[i][j-1]==0 and laberinto[i-1][j-1]==0 and laberinto[i-1][j]==0):
                    laberinto[i][j] = 1
    return laberinto

def ponerMuro(laberinto,i,j,estado):
    #pickDR{down,right,downright}
    if(estado == "centro"):
        pickDR = random.randint(1,3)
        if(pickDR == 1):
            laberinto[i+1][j] = 1
        elif(pickDR == 2):
            if(espaciosBlancoMuro(laberinto,i,j+1)):
                laberinto[i][j+1] = 1
        elif(pickDR == 3):
            if(espaciosBlancoMuro(laberinto,i,j+1)):
                laberinto[i][j-1] = 1
                laberinto[i+1][j] = 1
        return 0
    elif(estado == "abajo"):
        pickDR = random.randint(0,1)
        if(pickDR == 1):
            if(espaciosBlancoMuro(laberinto,i,j+1)):
                laberinto[i][j+1] = 1
        return 0
        
        

def marcoLaberinto(laberinto, height, width):
    for i in range(0,height):
        for j in range(0,width):
            if(i==0 or i==height-1):
                laberinto[i][j] = 1
            elif(j==0 or j==width-1):
                laberinto[i][j] = 1
    return laberinto

def espaciosBlancoMuro(laberinto,i,j):
    if(laberinto[i-1][j+1] == 0 and laberinto[i][j+1] == 0):
        return True
    else:
        return False
        
        
def printMatrix(testMatrix):
        for i, element in enumerate(testMatrix):
              print ' '.join(str(element))
              

def main():
    laberinto = [[0 for _ in range((WIDTH))] for _ in range((HEIGHT))]
    laberinto = marcoLaberinto(laberinto,HEIGHT,WIDTH)
    laberinto = generacionAleatoria(laberinto,HEIGHT,WIDTH)
    printMatrix(laberinto)
    
    
if __name__ == '__main__':
    main()