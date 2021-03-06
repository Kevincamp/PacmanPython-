import pygame
import abc
import math
from collections import deque
import sys, copy, random, os, time
global segundos,contadorGalletas, contadorGalletasTotal,banderaModoJuego
# banderaModoJuego == 0: Solucion juego es DFS
# banderaModoJuego == 1: Solucion juego es BFS
segundos = 0
contadorGalletas = 0
contadorGalletasTotal = 0
MAX = 15


# -- Funciones Generales ------------------------------------------------------------------

imagenes = {}
def cargar_imagen ( fichero_imagen ):
    global imagenes
    imagen = imagenes.get ( fichero_imagen, None )
    if imagen is None:
        imagen = pygame.image.load(os.path.join("imagenes",fichero_imagen)).convert()
        imagenes[fichero_imagen] = imagen
        imagen.set_colorkey (  imagen.get_at((0,0)) , pygame.RLEACCEL )
    return imagen

sonidos = {}
def cargar_sonido ( fichero_sonido ):
    global sonidos
    sonido = sonidos.get ( fichero_sonido, None )
    if sonido is None:
        sonido = pygame.mixer.Sound ( os.path.join ("sonidos", fichero_sonido))
        sonidos[fichero_sonido] = sonido
    return sonido    

def text_objects(text, font):
    textSurface = font.render(text, True, [255,255,0])
    return textSurface, textSurface.get_rect()
    
def text_objects_2(text, font):
    textSurface = font.render(text, True, [0,0,0])
    return textSurface, textSurface.get_rect()

def text_objects_3(text, font):
    textSurface = font.render(text, True, [255,255,255])
    return textSurface, textSurface.get_rect()

def ManejarEventos():
    global eventos # explicitamente declaramos que "eventos" es una variable global
    eventos = pygame.event.get()
    for event in eventos:
        if event.type == pygame.QUIT: 
            sys.exit(0) #se termina el programa
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print event.pos

# -- Fin de funciones Generales -------------------------------------------------------------

#--- Inicio de Clase de Estado --------------------------------------------
class Estado(object):
    def __init__(self,posx,posy,dist):
        self.posx = posx 
        self.posy = posy
        self.dist = dist 
     
#--- Fin de Clase de Estado --------------------------------------------

#--- Fin de Clase de Casilla --------------------------------------------

class Casilla():
    def __init__(self, tipo):
        self.visitado = 0
        self.direccion = ''
        self.tipo = tipo
        self.x = 0
        self.y = 0
        self.Pared_x = 0
        self.Pared_y = 0
        self.posPadrex = 0
        self.posPadrey = 0
        self.esfuerzo = 10
        self.heuristica = 0
        self.valor = 100
    def set_visitado(self):
        self.visitado = 1
    def set_direccion(self, direccion):
        self.direccion = direccion
    def set_x_y(self,x,y):
        self.x = x
        self.y = y
    def set_pared(self,pared_x,pared_y):
        self.Pared_x = pared_x
        self.Pared_y = pared_y
    def set_padre(self,posPadrex,posPadrey):
        self.posPadrex = posPadrex
        self.posPadrey = posPadrey
    def set_heuristica(self,x,y,goalx,goaly):
        #self.heuristica = round(math.sqrt(abs(goalx-x) + abs(goaly-y)))
        self.heuristica = math.sqrt(abs(goalx-x) + abs(goaly-y))
    def set_valor(self):
        self.valor = self.esfuerzo + self.heuristica
    def set_valorMax(self):
        self.valor = 100

#--- Fin de Clase de Casilla --------------------------------------------
    
#--- Inicio MiSprite -----------------------------------------------            

class MiSprite ( pygame.sprite.Sprite ):
    '''Todos los objetos que se representan en pantalla son sprites'''
    def __init__(self, fichero_imagen = None, pos_inicial = [0,0]):
        pygame.sprite.Sprite.__init__(self) 
        
        #Un sprite debe tener definida las propiedades "image" y "rect"
        #    Image representa la imagen a visualizar. Es de tipo "surface".
        #    Rect es un rectangulo que representa la zona de la pantalla que ocupara la imagen
        if not fichero_imagen is None:
            self.image = cargar_imagen(fichero_imagen)
            self.rect = self.image.get_rect()
            self.rect.topleft = pos_inicial
        
    def update (self):
        pygame.sprite.Sprite.update ( self )
#--- Fin MiSprite -----------------------------------------------  

#--- Inicio SpriteMovil --------------------------------------------  

class SpriteMovil ( MiSprite ):
    def __init__(self, fichero_imagen, pos_inicial, velocidad):
        MiSprite.__init__(self, fichero_imagen, pos_inicial) 
        self.rect.topleft = pos_inicial
        self.velocidad = velocidad
        
    def update (self):       
        #la funcion "copy" crea una copia del rectangulo  
        copia_rect = copy.copy(self.rect)
       
        self.rect.move_ip ( self.velocidad[0], self.velocidad[1]) 
       
        colisiones = pygame.sprite.spritecollide(self, sprites, False)
        for colision in colisiones:
            if colision != self:
                if hasattr ( colision, "infranqueable" ):
                    if colision.infranqueable:
                        self.velocidad[0]=0
                        self.velocidad[1]=0
                        self.rect = copia_rect
                        return     
            
        screen = pygame.display.get_surface () 
            
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocidad[1] = 0
        elif self.rect.bottom > screen.get_height():
            self.rect.bottom = screen.get_height()
            self.velocidad[1] = 0
            
        if self.rect.left < 0:
            self.rect.left = 0
            self.velocidad[0] = 0
        elif self.rect.right > screen.get_width():
            self.rect.right = screen.get_width()
            self.velocidad[0] = 0
          
#--- Fin SpriteMovil -----------------------------------------------  

#--- Inicio Laberinto -------------------------------------------

class Laberinto():
    posicionSalida = []
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
        for i in range(2,height-1):
            for j in range(1,width-1):   
                    if(laberinto[i][j]==0 and laberinto[i][j-1]==0 and laberinto[i-1][j-1]==0 and laberinto[i-1][j]==0 and laberinto[i-1][j+1]==0 and laberinto[i][j+1]==0):
                        laberinto[i][j] = 1
                        if(i!=height-3):
                            self.ponerMuro(laberinto,i,j,"centro")
                        else:
                            self.ponerMuro(laberinto,i,j,"centropenultimo")
                    elif(laberinto[i][j]==0 and laberinto[i][j-1]==0 and laberinto[i-1][j-1]==0 and laberinto[i-1][j]==0):
                        laberinto[i][j] = 1
                    elif(laberinto[i][j] == 0 and laberinto[i][j-1]==1 and laberinto[i-1][j]==1 and i==height-2 and j==width-2):
                        laberinto[i][j] = 1
        return laberinto
    
    def ponerMuro(self,laberinto,i,j,estado):
        #pickDR{down,right,downright}
        if(estado == "centro"):
            pickDR = random.randint(1,2)
            if(pickDR == 1):
                laberinto[i+1][j] = 1
            elif(pickDR == 2):
                if(self.espaciosBlancoMuro(laberinto,i,j+1)):
                    laberinto[i][j+1] = 1
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
        selectorLista = [1,2,3,4]
        for j in range (0,width):
            if(laberinto[1][j]==0):
                murosSalidaUP.append(j)
        for i in range (0,height):
            if(laberinto[i][1]==0):
                murosSalidaLEFT.append(i)
            elif(laberinto[i][width-2]==0):
                murosSalidaRIGHT.append(i)
                
        selector = random.choice(selectorLista)        
        validator = 0
        while validator == 0:
            if(selector == 1):
                if(len(murosSalidaUP)!=0):
                    muroSalida = random.choice(murosSalidaUP)
                    laberinto[0][muroSalida] = 0
                    self.posicionSalida = [0,muroSalida]
                    validator = 1
                else:
                    selectorLista.remove(selector)
                    selector = random.choice(selectorLista)
            elif(selector == 2):
                if(len(murosSalidaDOWN)!=0):
                    muroSalida = random.choice(murosSalidaDOWN)
                    laberinto[height-1][muroSalida] = 0
                    self.posicionSalida = [height-1,muroSalida]
                    validator = 1
                else:
                    selectorLista.remove(selector)
                    selector = random.choice(selectorLista)
            elif(selector == 3):
                if(len(murosSalidaLEFT)!=0):
                    muroSalida = random.choice(murosSalidaLEFT)
                    laberinto[muroSalida][0] = 0
                    self.posicionSalida = [muroSalida,0]
                    validator = 1
                else:
                    selectorLista.remove(selector)
                    selector = random.choice(selectorLista)
            else:
                if(len(murosSalidaRIGHT)!=0):
                    muroSalida = random.choice(murosSalidaRIGHT)
                    laberinto[muroSalida][width-1] = 0
                    self.posicionSalida = [muroSalida,width-1]
                    validator = 1
                else:
                    selectorLista.remove(selector)
                    selector = random.choice(selectorLista)
        return 0

#--- Fin Laberinto -------------------------------------------

# -- Inicio GAME OVER -----------------------------------------------------------------------------

def esMeta(pacman):
    if (pacman.rect.left >= finish[0] and pacman.rect.left <= finish[0]+25 and pacman.rect.top <= finish[1]+25 ):
        return 1
    return 0

def game_over(pacman):
    'El juego finaliza cuando se haya comido todas las galletas y cuando se encuentre en la salida'
    existen_galletas= esta_enla_salida = False
    if (contadorGalletas == contadorGalletasTotal and esMeta(pacman)==1):
        existen_galletas = True
    
    return not ( existen_galletas)
# -- Fin GAME OVER -----------------------------------------------------------------------------

# -- Inicio Marcador ---------------------------------------------------------

class Tiempo (MiSprite):
    def __init__(self):
        MiSprite.__init__(self)
        self.font = pygame.font.SysFont("Arial", 20)
        self.rect = pygame.rect.Rect(0,0,0,0)

    
    def update(self):

        self.tiempo = "Tiempo: %d " %(segundos) 
        self.image = self.font.render(self.tiempo, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        
        #situamos al marcador en la esquina superior derecha
        self.rect.topleft = (760,20)

        MiSprite.update (self)

class Comida (MiSprite):
    def __init__(self):
        MiSprite.__init__(self)
        self.font = pygame.font.SysFont("Arial", 30)
        self.rect = pygame.rect.Rect(0,0,0,0)
        
    def update(self):
        self.texto = "Galletas: %d " % (contadorGalletas)
        self.image = self.font.render(self.texto, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        
        #situamos al marcador en la esquina superior derecha
        self.rect.topleft = (760,50)
        
        MiSprite.update (self)
# -- Fin Marcador ------------------------------------------------------------

#--- Inicio Pared ---------------------------------------------

class Pared ( MiSprite ):
    def __init__(self, fichero_imagen, pos_inicial, dimension):
        MiSprite.__init__(self)
    
        self.image = pygame.Surface(dimension) #creamos una superficie de las dimensiones indicadas
        if not fichero_imagen is None:
            self.image = cargar_imagen(fichero_imagen)
            self.rect = self.image.get_rect()
            self.rect.topleft = pos_inicial
            self.infranqueable = True

    
    def update(self):
        MiSprite.update(self)

#--- Fin Pared ---------------------------------------------

#--- Inicio de Clase de Block --------------------------------------------

class Block ( MiSprite ):
    def __init__(self, color, pos_inicial):
        MiSprite.__init__(self)
        self.image = pygame.Surface([50, 50])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos_inicial
        self.infranqueable = False


    def update(self):
        MiSprite.update(self)

#--- Fin de Clase de Block --------------------------------------------

#-- Inicio track img-------------------------------------------

class Track ( MiSprite ):
    def __init__(self, fichero_imagen, pos_inicial, dimension):
        MiSprite.__init__(self)

        self.image = pygame.Surface(dimension) #creamos una superficie de las dimensiones indicadas
        if fichero_imagen is not None:
            self.image = cargar_imagen(fichero_imagen)
            self.rect = self.image.get_rect()
            self.rect.topleft = pos_inicial
            self.infranqueable = False


    def update(self):
        MiSprite.update(self)

#--- Inicio Pacman -----------------------------------------------            

class Pacman ( SpriteMovil ):
    NUMERO_FOTOGRAMAS = 8
    
    def __init__(self, fichero_imagen, pos_inicial):
        SpriteMovil.__init__(self, fichero_imagen, pos_inicial, [1,0]) 
        self.vidas = 3
        self.puntos = 0
        self.disparos = 2
        self.mover = 0
        self.__imagenArriba = {}
        self.__imagenAbajo = {}
        self.__imagenDerecha = {}
        self.__imagenIzquierda = {}
        
        for i in range(0, self.NUMERO_FOTOGRAMAS, 1):
            self.__imagenIzquierda[i] = cargar_imagen("pacman-izquierda" + str(i+1) + ".gif")
            self.__imagenDerecha[i] = cargar_imagen("pacman-derecha" + str(i+1) + ".gif")
            self.__imagenArriba[i] = cargar_imagen("pacman-arriba" + str(i+1) + ".gif")
            self.__imagenAbajo[i] = cargar_imagen("pacman-abajo" + str(i+1) + ".gif")
        
        self.__fotogramasActuales = self.__imagenDerecha
        self.__fotogramaActual = 1
        self.__tiempoCambioFotograma = pygame.time.get_ticks()

    def Movupdate (self,movimiento):
        #global eventos # explicitamente declaramos que "eventos" es una variable global
        global sprites
        global contadorGalletas
        v = 5
        for event in eventos:
            if movimiento == abajo:
                if movimiento == izquierda:
                    self.mover = 1
                    self.velocidad[0] = -v
                    self.velocidad[1] = 0
                elif movimiento == derecha:
                    self.mover = 1
                    self.velocidad[0] = v
                    self.velocidad[1] = 0
                elif movimiento == arriba:
                    self.mover = 1
                    self.velocidad[1] = -v
                    self.velocidad[0] = 0
                elif movimiento == abajo:
                    self.mover = 1
                    self.velocidad[1] = v
                    self.velocidad[0] = 0
                    
        if self.mover == 1:
            SpriteMovil.update(self)
            
            #se cambia la imagen de pacman segun la direccion
            if self.velocidad[0] > 0:
                self.__fotogramasActuales = self.__imagenDerecha
            elif self.velocidad[0] < 0:
                self.__fotogramasActuales = self.__imagenIzquierda
            elif self.velocidad[1] > 0:
                self.__fotogramasActuales = self.__imagenAbajo
            elif self.velocidad[1] < 0:
                self.__fotogramasActuales = self.__imagenArriba        
           
            if pygame.time.get_ticks() - self.__tiempoCambioFotograma > 50:
                self.__fotogramaActual = (self.__fotogramaActual + 1) % self.NUMERO_FOTOGRAMAS 
                self.__tiempoCambioFotograma = pygame.time.get_ticks()
            self.image = self.__fotogramasActuales[self.__fotogramaActual]
            
             
            #se obtiene todos los sprites con los que colisiona. El ultimo parametro indica que no queremos destruir automaticamente los sprites con los que colisiona 
            MiSprite.update(self) 
            
            #global sprites
            sprites_choque = pygame.sprite.spritecollide(self, sprites, False)
            
            for sprite in sprites_choque:
                if sprite != self:
                    if hasattr ( sprite, "comestible" ): #comprobamos si el sprite tiene un atributo llamado "comestible"
                        if sprite.comestible:
                            contadorGalletas = contadorGalletas + 1
                            sprite.kill() # destruimos el sprite
                            #if hasattr ( sprite, "puntos" ):
                             #   self.puntos += sprite.puntos
                              #  informar ( self.rect.bottomright, "puntos %d" % (sprite.puntos) )
        


    def update (self, direccion):
        #global eventos # explicitamente declaramos que "eventos" es una variable global
        global sprites
        global contadorGalletas
        v = 1
        # for event in eventos:
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_LEFT:
        #             self.mover = 1
        #             self.velocidad[0] = -v
        #             self.velocidad[1] = 0
        #         elif event.key == pygame.K_RIGHT:
        #             self.mover = 1
        #             self.velocidad[0] = v
        #             self.velocidad[1] = 0
        #         elif event.key == pygame.K_UP:
        #             self.mover = 1
        #             self.velocidad[1] = -v
        #             self.velocidad[0] = 0
        #         elif event.key == pygame.K_DOWN:
        #             self.mover = 1
        #             self.velocidad[1] = v
        #             self.velocidad[0] = 0
        for i in range(0,50):
            if direccion == 'izquierda':
                self.mover = 1
                self.velocidad[0] = -v
                self.velocidad[1] = 0
            elif direccion == 'derecha':
                self.mover = 1
                self.velocidad[0] = v
                self.velocidad[1] = 0
            elif direccion == 'arriba':
                self.mover = 1
                self.velocidad[1] = -v
                self.velocidad[0] = 0
            elif direccion == 'abajo':
                self.mover = 1
                self.velocidad[1] = v
                self.velocidad[0] = 0

            if self.mover == 1:
                SpriteMovil.update(self)

                #se cambia la imagen de pacman segun la direccion
                if self.velocidad[0] > 0:
                    self.__fotogramasActuales = self.__imagenDerecha
                elif self.velocidad[0] < 0:
                    self.__fotogramasActuales = self.__imagenIzquierda
                elif self.velocidad[1] > 0:
                    self.__fotogramasActuales = self.__imagenAbajo
                elif self.velocidad[1] < 0:
                    self.__fotogramasActuales = self.__imagenArriba

                if pygame.time.get_ticks() - self.__tiempoCambioFotograma > 50:
                    self.__fotogramaActual = (self.__fotogramaActual + 1) % self.NUMERO_FOTOGRAMAS
                    self.__tiempoCambioFotograma = pygame.time.get_ticks()
                self.image = self.__fotogramasActuales[self.__fotogramaActual]


                #se obtiene todos los sprites con los que colisiona. El ultimo parametro indica que no queremos destruir automaticamente los sprites con los que colisiona
                MiSprite.update(self)

                #global sprites
                sprites_choque = pygame.sprite.spritecollide(self, sprites, False)

                for sprite in sprites_choque:
                    if sprite != self:
                        if hasattr ( sprite, "comestible" ): #comprobamos si el sprite tiene un atributo llamado "comestible"
                            if sprite.comestible:
                                contadorGalletas = contadorGalletas + 1
                                sprite.kill() # destruimos el sprite
                                #if hasattr ( sprite, "puntos" ):
                                 #   self.puntos += sprite.puntos
                                  #  informar ( self.rect.bottomright, "puntos %d" % (sprite.puntos) )
        

#--- Fin Pacman -----------------------------------------------     

# -- Inicio de Juego ---------------------------------------------------------------------------------

def juego(numeroLaberinto):
    global banderaModoJuego
    global finish
    global contadorGalletas
    global mover
    global contadorGalletasTotal
    global segundos
    t = time.time()
    cicloCreado = 1
    
    visitado = []
    for i in range(15):
        visitado.append([])
        for j in range(15):
            visitado[i].append(False)
    
    laberinto1 =    [[1,1,1,1,1,1,1,1,1,1,0,1,1,1,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,1,1,1,1,1,1,1,1,1,0,1,0,1],
                    [1,0,0,0,0,0,0,1,0,0,0,0,1,0,1],
                    [1,0,1,1,0,1,0,1,0,1,1,1,1,0,1],
                    [1,0,1,1,0,1,0,1,0,1,0,0,0,0,1],
                    [1,0,1,1,0,1,0,0,0,0,0,1,0,1,1],
                    [1,0,0,0,0,1,0,1,1,1,1,1,0,1,1],
                    [1,0,1,0,1,0,0,0,0,0,0,0,0,1,1],
                    [1,0,1,0,1,0,1,0,1,0,1,1,0,1,1],
                    [1,0,0,0,0,0,1,0,1,0,0,0,0,0,1],
                    [1,0,1,1,1,0,1,0,1,0,1,1,1,0,1],
                    [1,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
                    [1,1,1,0,2,0,1,1,1,0,0,0,1,1,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

    laberinto2 =    [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,1,1,1,1,0,1,1,0,1,0,1,0,1],
                    [1,0,0,0,0,1,0,0,0,0,1,0,1,0,1],
                    [1,0,1,1,0,1,0,1,1,0,1,0,0,0,1],
                    [1,0,0,0,0,1,0,0,0,0,1,1,0,1,1],
                    [0,0,1,0,1,1,0,1,1,0,1,0,0,1,1],
                    [1,0,1,0,0,0,0,0,0,0,1,1,0,0,1],
                    [1,0,1,0,1,1,1,1,1,0,0,0,0,1,1],
                    [1,0,1,0,1,0,0,0,0,0,1,0,1,1,1],
                    [1,0,1,0,0,0,1,0,1,1,1,0,1,1,1],
                    [1,0,0,0,1,0,1,0,0,0,0,0,0,1,1],
                    [1,0,1,1,1,0,1,0,1,1,1,1,0,1,1],
                    [1,0,0,0,0,0,1,0,0,0,0,0,0,2,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

    laberinto3 =    [[1,1,1,1,1,1,1,1,1,1,1,1,0,1,1],
                    [1,2,1,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,1,0,1,1,1,1,1,0,1,0,1,1,1],
                    [1,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
                    [1,0,0,0,1,0,1,0,1,0,0,0,1,0,1],
                    [1,0,1,0,1,0,1,0,1,0,1,1,1,0,1],
                    [1,0,1,0,1,0,0,0,1,0,1,0,0,0,1],
                    [1,0,1,0,1,1,0,1,1,0,1,0,1,0,1],
                    [1,0,1,0,0,0,0,0,0,0,1,0,1,0,1],
                    [1,0,0,0,1,1,1,1,1,0,0,0,1,0,1],
                    [1,0,1,0,0,0,0,0,0,0,1,0,1,0,1],
                    [1,0,1,0,1,1,0,1,1,0,1,0,1,0,1],
                    [1,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,1,1,1,0,1,1,1,0,1,1,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

    laberinto4 =    [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,0,0,0,0,0,0,0,0,1,0,1,1,0,1],
                    [1,0,1,1,0,1,1,1,0,1,0,1,1,0,1],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,1,1,0,1,0,1,1,1,0,1,1,0,1],
                    [1,0,0,0,0,1,0,0,0,1,0,0,0,0,1],
                    [1,1,0,1,1,1,1,1,0,1,0,1,1,1,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,1,0,1,0,1,1,1,0,1,0,1,1,0,1],
                    [1,0,0,1,0,0,0,1,0,1,0,0,0,0,1],
                    [1,0,1,1,0,1,0,1,0,1,0,1,1,0,1],
                    [1,0,0,0,2,1,0,0,0,0,0,1,1,0,1],
                    [1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
                    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

    laberinto5 =    [[1,1,1,1,1,1,1,1,1,1,1,0,1,1,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
                    [1,0,1,0,0,0,0,0,1,0,1,0,1,0,1],
                    [1,0,1,1,1,1,1,1,1,0,1,0,1,1,1],
                    [1,0,1,0,0,0,0,0,0,0,0,0,1,0,1],
                    [1,0,1,1,1,1,1,1,1,1,1,0,1,0,1],
                    [1,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
                    [1,0,1,1,1,1,1,0,1,1,1,0,1,1,1],
                    [1,0,1,0,1,0,1,0,1,0,0,0,1,2,1],
                    [1,0,1,0,1,0,1,0,1,1,0,1,1,0,1],
                    [1,0,1,0,1,0,0,0,0,1,0,0,1,0,1],
                    [1,0,1,0,1,1,1,1,1,1,1,1,1,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

    laberinto6 =    [[1,1,1,0,1,1,1,1,1,1,1,1,1,1,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,1,0,1,1,1,0,1,1,1,1,0,1,1,1],
                    [1,1,0,1,0,0,0,1,1,1,1,0,0,0,1],
                    [1,1,0,1,0,1,0,1,1,1,1,0,1,0,1],
                    [1,0,0,0,0,1,0,0,0,0,0,0,1,0,1],
                    [1,1,0,1,1,1,1,1,0,1,0,1,1,1,1],
                    [1,1,0,0,0,0,0,0,0,1,0,0,0,0,1],
                    [1,1,0,1,1,1,0,1,1,1,1,1,0,1,1],
                    [1,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,1,1,0,1,1,1,0,1,0,1,1,1,1],
                    [1,0,1,1,0,1,0,0,0,1,0,0,0,0,1],
                    [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

    # laberinto7 =    [[1,1,1,0,1,1,1,1,1,1,1,1,1,1,1],
    #                 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    #                 [1,0,1,1,0,1,0,1,0,1,1,0,1,0,1],
    #                 [1,0,0,0,0,1,0,1,0,0,0,0,0,0,1],
    #                 [1,0,1,0,1,0,0,0,0,1,1,0,1,0,1],
    #                 [1,0,1,0,0,0,1,1,0,0,0,0,1,0,1],
    #                 [1,0,0,0,1,0,0,0,0,1,0,1,0,0,1],
    #                 [1,0,1,0,0,0,1,0,1,1,0,0,0,1,1],
    #                 [1,0,1,0,1,0,1,0,0,0,0,1,0,0,1],
    #                 [1,0,0,0,1,0,0,0,1,1,0,1,0,1,1],
    #                 [1,0,1,0,0,0,1,0,0,0,0,0,0,0,1],
    #                 [1,0,1,0,1,0,1,0,1,0,1,1,0,1,1],
    #                 [1,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
    #                 [1,0,1,1,0,1,1,0,0,0,1,1,0,1,1],
    #                 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
    #
    # laberinto8 =    [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    #                 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    #                 [1,0,1,1,0,1,1,0,1,1,0,1,0,1,1],
    #                 [1,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
    #                 [1,0,1,1,0,1,0,1,0,1,0,0,0,1,1],
    #                 [1,0,0,0,0,1,0,1,0,1,0,1,0,0,1],
    #                 [1,0,1,0,1,0,0,0,0,0,0,0,0,1,1],
    #                 [0,0,1,0,0,0,1,0,1,1,0,1,0,0,1],
    #                 [1,0,0,0,1,0,1,0,0,0,0,1,0,1,1],
    #                 [1,0,1,0,0,0,0,0,1,0,1,0,0,0,1],
    #                 [1,0,0,0,1,0,1,0,1,0,0,0,1,0,1],
    #                 [1,0,1,0,1,0,0,0,0,0,1,0,1,0,1],
    #                 [1,0,0,0,0,0,1,1,0,1,1,0,0,0,1],
    #                 [1,0,1,0,1,0,0,0,0,0,0,0,1,0,1],
    #                 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
    #
    # laberinto9 =    [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    #                 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    #                 [1,0,1,1,0,1,1,0,1,0,1,0,1,0,1],
    #                 [1,0,0,0,0,0,0,0,1,0,1,0,0,0,1],
    #                 [1,0,1,1,0,1,0,1,0,0,0,0,1,0,1],
    #                 [1,0,0,0,0,1,0,0,0,1,1,0,0,0,1],
    #                 [1,0,1,0,1,0,0,1,0,0,0,0,1,0,1],
    #                 [1,0,1,0,0,0,1,0,0,1,1,0,0,0,1],
    #                 [1,0,0,0,1,0,0,0,1,0,0,0,1,0,1],
    #                 [1,0,1,0,1,0,1,0,0,0,1,0,1,0,1],
    #                 [1,0,0,0,0,0,1,0,1,0,0,0,0,0,1],
    #                 [1,0,1,0,1,0,0,0,1,0,1,1,0,1,1],
    #                 [1,0,1,0,0,0,1,0,0,0,0,0,0,0,1],
    #                 [0,0,0,0,1,0,0,0,1,0,1,1,0,1,1],
    #                 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
    #
    # laberinto10 =   [[1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
    #                 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    #                 [1,0,1,0,1,1,0,1,0,1,1,0,1,0,1],
    #                 [1,0,1,0,0,0,0,1,0,0,0,0,1,0,1],
    #                 [1,0,0,0,1,1,0,0,0,1,0,1,0,0,1],
    #                 [1,0,1,0,0,0,0,1,0,1,0,0,0,1,1],
    #                 [1,0,0,0,1,1,0,1,0,0,0,1,0,0,1],
    #                 [1,0,1,0,0,0,0,0,0,1,0,1,0,1,1],
    #                 [1,0,0,0,1,0,1,1,0,1,0,0,0,0,1],
    #                 [1,0,1,0,1,0,0,0,0,0,0,1,0,1,1],
    #                 [1,0,0,0,0,0,1,1,0,1,0,1,0,0,1],
    #                 [1,0,1,0,1,0,0,0,0,0,0,0,0,1,1],
    #                 [1,0,1,0,1,0,1,1,0,1,1,0,1,0,1],
    #                 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    #                 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

    posSalidaLab1 = [0,10]
    posSalidaLab2 = [6,0]
    posSalidaLab3 = [0,12]
    posSalidaLab4 = [3,0]
    posSalidaLab5 = [0,11]
    posSalidaLab6 = [0,3]
    # posSalidaLab7 = [0,3]
    # posSalidaLab8 = [7,0]
    # posSalidaLab9 = [13,0]
    # posSalidaLab10 = [0,2]
    contadorGalletas = 0

    contadorGalletasTotal = 0
    finish = []
    
    Pared_x=0
    Salir = False
    Pared_y=0
    if numeroLaberinto == 0:
        maze = Laberinto(15,15)
        laberinto = maze.getMaze()
        posicionSalida = maze.posicionSalida
    if numeroLaberinto == 1:
        laberinto = laberinto1
        posicionSalida = posSalidaLab1
    if numeroLaberinto == 2:
        laberinto = laberinto2
        posicionSalida = posSalidaLab2
    if numeroLaberinto == 3:
        laberinto = laberinto3
        posicionSalida = posSalidaLab3
    if numeroLaberinto == 4:
        laberinto = laberinto4
        posicionSalida = posSalidaLab4
    if numeroLaberinto == 5:
        laberinto = laberinto5
        posicionSalida = posSalidaLab5
    if numeroLaberinto == 6:
        laberinto = laberinto6
        posicionSalida = posSalidaLab6
    # if numeroLaberinto == 7:
    #     laberinto = laberinto7
    #     posicionSalida = posSalidaLab7
    # if numeroLaberinto == 8:
    #     laberinto = laberinto8
    #     posicionSalida = posSalidaLab8
    # if numeroLaberinto == 9:
    #     laberinto = laberinto9
    #     posicionSalida = posSalidaLab9
    # if numeroLaberinto == 10:
    #     laberinto = laberinto10
    #     posicionSalida = posSalidaLab10

    screen = pygame.display.get_surface()
    screen.fill((0,0,0))
    pygame.display.update()
    #creamos una copia de la pantalla para evitar su repintado completo cuando
    #se redibujen los sprites
    background = screen.copy()
    #bucle de redibujado de los screens
    for i in range(15):
            for j in range(15):  
                if(laberinto[i][j] == 1):
                    laberinto[i][j] = Casilla('muro')
                    laberinto[i][j].set_x_y(i,j)
                    laberinto[i][j].set_pared(Pared_x,Pared_y)
                    sprite = Pared ( "wall.png", [Pared_x,Pared_y], [50,50] )
                    sprites.add (sprite)
                    Pared_x+=50
                elif (laberinto[i][j] == 2):
                    laberinto[i][j]= Casilla('meta')
                    xmeta = i
                    ymeta = j
                    laberinto[i][j].set_x_y(i,j)
                    laberinto[i][j].set_pared(Pared_x,Pared_y)
                    sprite = MiSprite ("bola.png", [Pared_x+15, Pared_y+15])
                    sprite.comestible = True
                    sprite.puntos = 5
                    sprites.add ( sprite )
                    contadorGalletasTotal +=1
                    Pared_x+=50
                else:
                    if(i ==posicionSalida[0] and j==posicionSalida[1]):
                        laberinto[i][j] = Casilla('salida')
                        laberinto[i][j].set_x_y(i,j)
                        laberinto[i][j].set_pared(Pared_x,Pared_y)
                        sprite = MiSprite ("finish.png", [Pared_x, Pared_y])
                        pacman = Pacman("pacman.gif", [Pared_x,Pared_y])
                        #Mando estado inicial de pacman.
                        inicial = Estado(Pared_x,Pared_y,0)
                        queue = deque([])
                        queue.append(inicial)
                        finish.append(Pared_x)
                        finish.append(Pared_y)
                        sprites.add ( sprite )
                        #sprites.add ( pacman )
                        Pared_x+=50
                    else:
                        laberinto[i][j] = Casilla('galleta')
                        laberinto[i][j].set_x_y(i,j)
                        laberinto[i][j].set_pared(Pared_x,Pared_y)
                        Pared_x+=50
            Pared_x=0
            Pared_y+=50
    
    
    
    sonido_fondo = cargar_sonido ("sonido_fondo.wav").play(-1) #este sonido se repetira indefinidamente al indicar -1 como parametro   
    eventos = pygame.event.get()
    bandera = 0
    banderaTiempo = 0

    x = posicionSalida[0]
    y = posicionSalida[1]
    x_i = posicionSalida[0]
    y_i = posicionSalida[1]
    
    #Algoritmo DFS inicializacion----------------------------------------
    dfs_stack = list()
    pop_list = list()
    dfs_stack.append(laberinto[x][y])
    #Fin DFS inicializacion----------------------------------------------
    #Algoritmo BFS inicializacion----------------------------------------
    bfs_stack = deque([laberinto[x][y]])
    bfs_goalPath = list()
    #Fin BFS inicializacion----------------------------------------------
    #Algoritmo A* inicializacion----------------------------------------
    aStar_goalPath = list()
    aStar_goalPath.append(laberinto[x][y])
    aStar_nodes = list()
    listaN = list()
    listaN.append(laberinto[x][y])
    #Fin A* inicializacion----------------------------------------------
    
    laberinto[x][y].set_visitado()
    sprite_trail = pygame.sprite.RenderUpdates()
    
    while game_over(pacman):
        if bandera == 0:
            tiempo = Tiempo ()
            sprites.add ( tiempo )
            bandera = 1
        if bandera == 1:
            if banderaTiempo == 0:
                inicio = pygame.time.get_ticks()/1000
                banderaTiempo = 1
            segundos = pygame.time.get_ticks()/1000 - inicio

        #Algoritmo DFS sentido Arriba - derecha - abajo - izquierda ---------------------------------------
        #for casilla in dfs_stack:
        #    print(casilla.direccion),
        #print('\n'+str(x)+' '+str(y))
        pygame.time.delay(250)
        if banderaModoJuego == 0 :
            #********************************************************Inicio Algoritmo DFS ---------------------------------------
            if laberinto[x-1][y].visitado == 0 and (laberinto[x-1][y].tipo == 'galleta' or laberinto[x-1][y].tipo == 'meta'):
                laberinto[x][y].set_direccion('arriba')
                sprite = Track ( "up.jpg", [laberinto[x][y].Pared_x,laberinto[x][y].Pared_y], [50,50] )
                sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
                sprites.add (sprite)
                if laberinto[x-1][y].tipo == 'meta':
                    break
                else:
                    laberinto[x-1][y].set_visitado()
                    dfs_stack.append(laberinto[x-1][y])
                x = x-1
            elif laberinto[x][y+1].visitado == 0 and (laberinto[x][y+1].tipo == 'galleta' or laberinto[x][y+1].tipo == 'meta'):
                laberinto[x][y].set_direccion('derecha')
                sprite = Track ( "right.jpg", [laberinto[x][y].Pared_x,laberinto[x][y].Pared_y], [50,50] )
                sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
                sprites.add (sprite)
                if laberinto[x][y+1].tipo == 'meta':
                    break
                else:
                    laberinto[x][y+1].set_visitado()
                    dfs_stack.append(laberinto[x][y+1])
                y = y+1
            elif laberinto[x+1][y].visitado == 0 and (laberinto[x+1][y].tipo == 'galleta' or laberinto[x+1][y].tipo == 'meta'):
                laberinto[x][y].set_direccion('abajo')
                sprite = Track ( "down.jpg", [laberinto[x][y].Pared_x,laberinto[x][y].Pared_y], [50,50] )
                sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
                sprites.add (sprite)
                if laberinto[x+1][y].tipo == 'meta':
                    break
                else:
                    laberinto[x+1][y].set_visitado()
                    dfs_stack.append(laberinto[x+1][y])
                x = x+1
            elif laberinto[x][y-1].visitado == 0 and (laberinto[x][y-1].tipo == 'galleta' or laberinto[x][y-1].tipo == 'meta'):
                laberinto[x][y].set_direccion('izquierda')
                sprite = Track ( "left.jpg", [laberinto[x][y].Pared_x,laberinto[x][y].Pared_y], [50,50] )
                sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
                sprites.add (sprite)
                if laberinto[x][y-1].tipo == 'meta':
                    break
                else:
                    laberinto[x][y-1].set_visitado()
                    dfs_stack.append(laberinto[x][y-1])
                y = y-1
            else:
                wrong_casilla = dfs_stack.pop()
                pop_list.append(wrong_casilla)
                if wrong_casilla.direccion == 'arriba':
                    sprite = Track ( "rup.jpg", [wrong_casilla.Pared_x,wrong_casilla.Pared_y], [50,50] )
                    sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
                    sprites.add (sprite)
                elif wrong_casilla.direccion == 'derecha':
                    sprite = Track ( "rright.jpg", [wrong_casilla.Pared_x,wrong_casilla.Pared_y], [50,50] )
                    sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
                    sprites.add (sprite)
                elif wrong_casilla.direccion == 'abajo':
                    sprite = Track ( "rdown.jpg", [wrong_casilla.Pared_x,wrong_casilla.Pared_y], [50,50] )
                    sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
                    sprites.add (sprite)
                elif wrong_casilla.direccion == 'izquierda':
                    sprite = Track ( "rleft.jpg", [wrong_casilla.Pared_x,wrong_casilla.Pared_y], [50,50] )
                    sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
                    sprites.add (sprite)
                else:
                    sprite = Track ( "x.jpg", [wrong_casilla.Pared_x,wrong_casilla.Pared_y], [50,50] )
                    sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
                    sprites.add (sprite)
                last_casilla = dfs_stack[-1]
                x = last_casilla.x
                y = last_casilla.y
            #********************************************************Fin Algoritmo DFS ---------------------------------------
        
        elif banderaModoJuego == 1 :
            #********************************************************Inicio Algoritmo BFS ---------------------------------------
            if bfs_stack: #Pregunto si la cola NO esta vacia
                proxCasilla = bfs_stack.popleft() # Saco el primero de la cola
                if proxCasilla.tipo == 'meta':
                    print 'Entro a es Meta'
                    x = proxCasilla.x
                    y = proxCasilla.y
                    #print '\nPosMetax:'+ str(x) + ',PosMetay:'+ str(y)
                    while(laberinto[x][y].posPadrex != 0 or laberinto[x][y].posPadrey != 0 ):
                        # Se almacenara mi camino de salida en bfs_goalPath siendo una lista
                        if laberinto[x][y].direccion != '':
                            bfs_goalPath.append(laberinto[x][y])

                        respaldox = x
                        respaldoy = y
                        x = laberinto[respaldox][respaldoy].posPadrex
                        y = laberinto[respaldox][respaldoy].posPadrey
                        if respaldox > x:
                            laberinto[x][y].set_direccion('abajo')
                        if respaldox < x:
                            laberinto[x][y].set_direccion('arriba')
                        if respaldoy > y:
                            laberinto[x][y].set_direccion('derecha')
                        if respaldoy < y:
                            laberinto[x][y].set_direccion('izquierda')
                     #   print'\nPosPadrex:'+ str(x) + ',PosPadrey:'+ str(y)

                    # Ordenandolos de nodo inicial+1 hasta final
                    bfs_goalPath.append(laberinto[x_i][y_i])
                    bfs_goalPath.reverse()
                    #anadiendo el nodo raiz
                    print '\nPosxinicial:'+str(x_i)+', Posyinicial:'+str(y_i)
                    
                    for lab in bfs_goalPath:
                        print lab.direccion
                    break
                else:
                    x = proxCasilla.x
                    y = proxCasilla.y
                    
                    if laberinto[x-1][y].visitado == 0 and (laberinto[x-1][y].tipo == 'galleta' or laberinto[x-1][y].tipo == 'meta'):
                        laberinto[x-1][y].set_padre(x,y)  
#                        print '\n******Posicion x: '+str(x-1)+ ', Posicion y: '+str(y)+' Padrex: '+str(x)+ ' Padrey: '+str(y)
                        laberinto[x][y].set_direccion('arriba')
                        sprite = Track ( "up.jpg", [laberinto[x][y].Pared_x,laberinto[x][y].Pared_y], [50,50] )
                        sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
                        sprites.add (sprite)
                        laberinto[x-1][y].set_visitado()
                        bfs_stack.append(laberinto[x-1][y])
                        
                    if laberinto[x][y+1].visitado == 0 and (laberinto[x][y+1].tipo == 'galleta' or  laberinto[x][y+1].tipo =='meta'):
                        laberinto[x][y+1].set_padre(x,y)
 #                       print '\n******Posicion x: '+str(x)+ ', Posicion y: '+str(y+1)+' Padrex: '+str(x)+ ' Padrey: '+str(y)
                        laberinto[x][y].set_direccion('derecha')
                        sprite = Track ( "right.jpg", [laberinto[x][y].Pared_x,laberinto[x][y].Pared_y], [50,50] )
                        sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
                        sprites.add (sprite)
                        laberinto[x][y+1].set_visitado()
                        bfs_stack.append(laberinto[x][y+1])

                    if laberinto[x+1][y].visitado == 0 and (laberinto[x+1][y].tipo == 'galleta' or laberinto[x+1][y].tipo=='meta'):
                        laberinto[x+1][y].set_padre(x,y)
                        #print '\n******Posicion x: '+str(x+1)+ ', Posicion y: '+str(y)+' Padrex: '+str(x)+ ' Padrey: '+str(y)
                        laberinto[x][y].set_direccion('abajo')
                        sprite = Track ( "down.jpg", [laberinto[x][y].Pared_x,laberinto[x][y].Pared_y], [50,50] )
                        sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
                        sprites.add (sprite)
                        laberinto[x+1][y].set_visitado()
                        bfs_stack.append(laberinto[x+1][y])

                    if laberinto[x][y-1].visitado == 0 and (laberinto[x][y-1].tipo == 'galleta' or laberinto[x][y-1].tipo=='meta'):
                        laberinto[x][y-1].set_padre(x,y)
   #                     print '\n******Posicion x: '+str(x)+', Posicion y: '+str(y-1)+' Padrex: '+str(x)+ ' Padrey: '+str(y)
                        laberinto[x][y].set_direccion('izquierda')
                        sprite = Track ( "left.jpg", [laberinto[x][y].Pared_x,laberinto[x][y].Pared_y], [50,50] )
                        sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
                        sprites.add (sprite)
                        laberinto[x][y-1].set_visitado()
                        bfs_stack.append(laberinto[x][y-1])

                    if laberinto[x][y].direccion == '':
                        sprite = Track ( "x.jpg", [laberinto[x][y].Pared_x,laberinto[x][y].Pared_y], [50,50] )
                        sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
                        sprites.add (sprite)

            #********************************************************Fin Algoritmo BFS ---------------------------------------
        elif banderaModoJuego == 2:
            #******************************************************** Inicio Algoritmo A* ---------------------------------------
            # Obteniendo Meta
            #print 'posMetaX:'+str(xmeta)+', posMetaY: '+str(ymeta)
            #Calculando Heuristica para cada movimiento de ser posible
            
            if laberinto[x-1][y].visitado == 0 and (laberinto[x-1][y].tipo == 'galleta' or laberinto[x-1][y].tipo == 'meta'):
                laberinto[x-1][y].set_heuristica(x-1,y,xmeta,ymeta)
                laberinto[x-1][y].set_valor()
            elif laberinto[x-1][y].visitado == 1:
                laberinto[x-1][y].set_valorMax()
                
            if laberinto[x][y+1].visitado == 0 and (laberinto[x][y+1].tipo == 'galleta' or laberinto[x][y+1].tipo == 'meta'):
                laberinto[x][y+1].set_heuristica(x,y+1,xmeta,ymeta)
                laberinto[x][y+1].set_valor()
            elif laberinto[x][y+1].visitado == 1:
                laberinto[x][y+1].set_valorMax()
                
            if laberinto[x+1][y].visitado == 0 and (laberinto[x+1][y].tipo == 'galleta' or laberinto[x+1][y].tipo == 'meta'):
                laberinto[x+1][y].set_heuristica(x+1,y,xmeta,ymeta)
                laberinto[x+1][y].set_valor()
            elif laberinto[x+1][y].visitado == 1:
                laberinto[x+1][y].set_valorMax()
                
            if laberinto[x][y-1].visitado == 0 and (laberinto[x][y-1].tipo == 'galleta' or laberinto[x][y-1].tipo == 'meta'):
                laberinto[x][y-1].set_heuristica(x,y-1,xmeta,ymeta)
                laberinto[x][y-1].set_valor()
            elif laberinto[x][y-1].visitado == 1:
                laberinto[x][y-1].set_valorMax()
                
            # ***********************************************************Escogiendo la mejor casilla y anadiendola a la lista
            # Procedimiento:
            # 1. Obtengo los valores de cada vecino y los coloco en una lista
                # Vaciando lista de nodos
            aStar_nodes = []
            
                # Metiendo los valores en la lista
            aStar_nodes.append(laberinto[x+1][y].valor)
            aStar_nodes.append(laberinto[x][y+1].valor)
            aStar_nodes.append(laberinto[x-1][y].valor)
            aStar_nodes.append(laberinto[x][y-1].valor)
            
            # 2. Ordeno la lista en orden Descendente ( Menor a Mayor )
            aStar_nodes.sort()
            listaN = listaN + aStar_nodes
            #listaN.extend(aStar_nodes)
            print aStar_nodes
            # 3. Voy recorriendo la lista para saber si ya ha sido visitado el nodo.
            # 4. El nodo que no ha sido visitado es escogido colocandolo en la lista aStar_goalPath y ejecutando movimiento
            encontrado = 0
            c = aStar_nodes[0]

            if c == laberinto[x+1][y].valor and laberinto[x+1][y].visitado == 0 and (laberinto[x+1][y].tipo == 'galleta' or laberinto[x+1][y].tipo == 'meta'):
                laberinto[x][y].set_direccion('abajo')
                encontrado = 1
                sprite = Track ( "down.jpg", [laberinto[x][y].Pared_x,laberinto[x][y].Pared_y], [50,50] )
                sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
                sprites.add (sprite)
                laberinto[x+1][y].set_visitado()                
                aStar_goalPath.append(laberinto[x+1][y])
                x = x + 1
                #break
                    
            elif c == laberinto[x][y+1].valor and laberinto[x][y+1].visitado == 0 and (laberinto[x][y+1].tipo == 'galleta' or laberinto[x][y+1].tipo == 'meta'):
                laberinto[x][y].set_direccion('derecha')
                encontrado = 1
                sprite = Track ( "right.jpg", [laberinto[x][y].Pared_x,laberinto[x][y].Pared_y], [50,50] )
                sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
                sprites.add (sprite)
                laberinto[x][y+1].set_visitado()
                aStar_goalPath.append(laberinto[x][y+1])
                y = y + 1
                #break
                    
            elif c == laberinto[x-1][y].valor and laberinto[x-1][y].visitado == 0 and (laberinto[x-1][y].tipo == 'galleta' or laberinto[x-1][y].tipo == 'meta'):
                laberinto[x][y].set_direccion('arriba')
                encontrado = 1
                sprite = Track ( "up.jpg", [laberinto[x][y].Pared_x,laberinto[x][y].Pared_y], [50,50] )
                sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
                sprites.add (sprite)
                laberinto[x-1][y].set_visitado()
                aStar_goalPath.append(laberinto[x-1][y])
                x = x - 1
                #break
                    
            elif c == laberinto[x][y-1].valor and laberinto[x][y-1].visitado == 0 and (laberinto[x][y-1].tipo == 'galleta' or laberinto[x][y-1].tipo == 'meta'):
                laberinto[x][y].set_direccion('izquierda')
                encontrado = 1
                sprite = Track ( "left.jpg", [laberinto[x][y].Pared_x,laberinto[x][y].Pared_y], [50,50] )
                sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
                sprites.add (sprite)
                laberinto[x][y-1].set_visitado()
                aStar_goalPath.append(laberinto[x][y-1])
                y = y - 1
                #break
                
                
                
            if encontrado==0:
                wrong_casilla = aStar_goalPath.pop()
                pop_list.append(wrong_casilla)
                if wrong_casilla.direccion == 'arriba':
                    sprite = Track ( "rup.jpg", [wrong_casilla.Pared_x,wrong_casilla.Pared_y], [50,50] )
                    sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
                    sprites.add (sprite)
                elif wrong_casilla.direccion == 'derecha':
                    sprite = Track ( "rright.jpg", [wrong_casilla.Pared_x,wrong_casilla.Pared_y], [50,50] )
                    sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
                    sprites.add (sprite)
                elif wrong_casilla.direccion == 'abajo':
                    sprite = Track ( "rdown.jpg", [wrong_casilla.Pared_x,wrong_casilla.Pared_y], [50,50] )
                    sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
                    sprites.add (sprite)
                elif wrong_casilla.direccion == 'izquierda':
                    sprite = Track ( "rleft.jpg", [wrong_casilla.Pared_x,wrong_casilla.Pared_y], [50,50] )
                    sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
                    sprites.add (sprite)
                else:
                    sprite = Track ( "x.jpg", [wrong_casilla.Pared_x,wrong_casilla.Pared_y], [50,50] )
                    sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
                    sprites.add (sprite)
                last_casilla = aStar_goalPath[-1]
                x = last_casilla.x
                y = last_casilla.y

                #else:
                    #Pilas listaN coja un elemento que no ha sido visitado.
                    #print 'else print'
                    #casilla = listaN[-1]
                    #print casilla.direccion
                    #casilla_erronea = listaN.pop()
                    #if casilla_erronea.visitado == 1:
                    #    casilla_erronea = listaN.pop()
                    #x = casilla_erronea.x
                    #y = casilla_erronea.y
                    #wrong_casilla = dfs_stack.pop()
                    #last_casilla = dfs_stack[-1]
                    #wrong_casillaA = listaN[-1]
                    
            if laberinto[x][y].tipo == 'meta':
                aStar_goalPath.append(laberinto[x][y])
                break

                
            #******************************************************** Fin Algoritmo A* ---------------------------------------
        reloj = pygame.time.Clock()
        ManejarEventos ()
        
        sprites.update ()
        sprites.clear (screen, background)
        
        pygame.display.update (sprites.draw (screen))
        if bandera == 1:
            reloj.tick (40) #tiempo de espera entre frames
    
    flag_blink = 0
    #Algoritmo DFS animacion
    if banderaModoJuego == 0:
        for i in range (0,10):
            if not flag_blink:
                list_sprites = list()
                for casilla in dfs_stack:
                    sprite = Block([0,0,0],[casilla.Pared_x,casilla.Pared_y])
                    sprite_temp = pygame.sprite.spritecollideany(sprite,sprites)
                    list_sprites.append(sprite_temp)
                    sprites.remove(sprite_temp)
                    sprites.add (sprite)
                flag_blink = 1
            else:
                for tmp_sprite in list_sprites:
                    sprites.remove(pygame.sprite.spritecollideany(tmp_sprite,sprites))
                    sprites.add (tmp_sprite)
                flag_blink = 0
            sprites.update ()
            sprites.clear (screen, background)
            pygame.display.update (sprites.draw (screen))
            pygame.time.delay(500)
            key_flag = 0
        while(True):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        key_flag = 1
            if key_flag == 1:
                break
        for casilla in dfs_stack:
            sprite = Block([0,0,0],[casilla.Pared_x,casilla.Pared_y])
            sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
        for casilla in pop_list:
            sprite = Block([0,0,0],[casilla.Pared_x,casilla.Pared_y])
            sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
        sprites.add ( pacman )
        sprites.clear (screen, background)
        pygame.display.update (sprites.draw (screen))
        for i in range(0,len(dfs_stack)):
            if i != 0:
                sprite = Block([0,0,100],[dfs_stack[i-1].Pared_x,dfs_stack[i-1].Pared_y])
                sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
                sprites.add(sprite)
            pacman.update(dfs_stack[i].direccion)
            sprites.clear (screen, background)
            pygame.display.update (sprites.draw (screen))
            pygame.time.delay(200)
    #Algoritmo BFS animacion
    elif banderaModoJuego == 1:
        for i in range (0,10):
            if not flag_blink:
                list_sprites = list()
                for casilla in bfs_goalPath:
                    sprite = Block([0,0,0],[casilla.Pared_x,casilla.Pared_y])
                    sprite_temp = pygame.sprite.spritecollideany(sprite,sprites)
                    list_sprites.append(sprite_temp)
                    sprites.remove(sprite_temp)
                    sprites.add (sprite)
                flag_blink = 1
            else:
                for tmp_sprite in list_sprites:
                    sprites.remove(pygame.sprite.spritecollideany(tmp_sprite,sprites))
                    sprites.add (tmp_sprite)
                flag_blink = 0
            sprites.update ()
            sprites.clear (screen, background)
            pygame.display.update (sprites.draw (screen))
            pygame.time.delay(500)
            key_flag = 0
        while(True):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        key_flag = 1
            if key_flag == 1:
                break
        for casilla in bfs_goalPath:
            sprite = Block([0,0,0],[casilla.Pared_x,casilla.Pared_y])
            sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
        sprites.add ( pacman )
        sprites.clear (screen, background)
        pygame.display.update (sprites.draw (screen))
        for i in range(0,len(bfs_goalPath)):
            if i != 0:
                sprite = Block([0,0,100],[bfs_goalPath[i-1].Pared_x,bfs_goalPath[i-1].Pared_y])
                sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
                sprites.add(sprite)
            pacman.update(bfs_goalPath[i].direccion)
            sprites.clear (screen, background)
            pygame.display.update (sprites.draw (screen))
            pygame.time.delay(200)
    #Algoritmo A* animacion
    elif banderaModoJuego == 2:
        for i in range (0,10):
            if not flag_blink:
                list_sprites = list()
                for casilla in aStar_goalPath:
                    sprite = Block([0,0,0],[casilla.Pared_x,casilla.Pared_y])
                    sprite_temp = pygame.sprite.spritecollideany(sprite,sprites)
                    list_sprites.append(sprite_temp)
                    sprites.remove(sprite_temp)
                    sprites.add (sprite)
                flag_blink = 1
            else:
                for tmp_sprite in list_sprites:
                    sprites.remove(pygame.sprite.spritecollideany(tmp_sprite,sprites))
                    sprites.add (tmp_sprite)
                flag_blink = 0
            sprites.update ()
            sprites.clear (screen, background)
            pygame.display.update (sprites.draw (screen))
            pygame.time.delay(500)
            key_flag = 0
        while(True):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        key_flag = 1
            if key_flag == 1:
                break
        for casilla in aStar_goalPath:
            sprite = Block([0,0,0],[casilla.Pared_x,casilla.Pared_y])
            sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
        sprites.add ( pacman )
        sprites.clear (screen, background)
        pygame.display.update (sprites.draw (screen))
        for i in range(0,len(aStar_goalPath)):
            if i != 0:
                sprite = Block([0,0,100],[aStar_goalPath[i-1].Pared_x,aStar_goalPath[i-1].Pared_y])
                sprites.remove(pygame.sprite.spritecollideany(sprite,sprites))
                sprites.add(sprite)
            pacman.update(aStar_goalPath[i].direccion)
            sprites.clear (screen, background)
            pygame.display.update (sprites.draw (screen))
            pygame.time.delay(200)
            key_flag = 0
    while(True):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    key_flag = 1
        if key_flag == 1:
            break
    #--el juego ha finalizado
    sprites.empty()   
    sonido_fondo.stop()
    pantallaGameOver()
     
    while True:
        eventos = pygame.event.get()
        ManejarEventos()

# -- Fin de Juego ------------------------------------------------------------------------------------
# -- Inicio de Pantalla ** GAME OVER ** ---------------------------------------------------

def pantallaGameOver():
    global contadorGalletas
    global segundos
    seAcabo = True
    while seAcabo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill([0,0,0])
        pygame.display.update(sprites.draw(screen))
    
        screen.fill ([0,0,0])
        largeText = pygame.font.SysFont("Arial", 120)
        TextSurf,TextRect = text_objects_3("GAME OVER",largeText)
        TextRect.center = (440,250)
        screen.blit(TextSurf,TextRect)
    
        largeText = pygame.font.SysFont("Arial", 80)
        texto = "Tiempo: %d seg." % (segundos)
        TextSurf,TextRect = text_objects_3(texto,largeText)
        TextRect.center = (450,400)
        screen.blit(TextSurf,TextRect)
    
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
    
        if (screen.get_width()*0.35) < mouse[0] < (screen.get_width()*0.35 +250) and (screen.get_height()*0.70) < mouse[1] < (screen.get_height()*0.70 + 60):
            pygame.draw.rect(screen, [192,255,192],(screen.get_width()*0.35,screen.get_height()*0.70,250,60))
            if click[0] == 1:
                pygame.mouse.set_pos((screen.get_width()*0.5),(screen.get_height()*0.5))
                menu_intro()
        else:
            pygame.draw.rect(screen, [0,255,0] , (screen.get_width()*0.35,screen.get_height()*0.70,250,60))
        mediumText = pygame.font.SysFont("Arial",40)
        textSurf_jugar,textRect_jugar = text_objects_2("Volver",mediumText)
        textRect_jugar.center = (screen.get_width()*0.49,screen.get_height()*0.735)
        screen.blit(textSurf_jugar,textRect_jugar)
     
        pygame.display.update()
# -- Fin de Pantalla de ** GAME OVER ** ---------------------------------------------------

# -- Inicio de Seleccion de definidos -------------------------------------------------------------

def menu_seleccion_definidos(intro):
    pygame.time.delay(250)
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        screen.fill([0,0,0])
        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        #Imagenes de Laberintos fijas
        juego1 = cargar_imagen("laberinto1.jpg")
        screen.blit(juego1,(40,20))
        juego2 = cargar_imagen("laberinto2.jpg")
        screen.blit(juego2,(340,20))
        juego3 = cargar_imagen("laberinto3.jpg")
        screen.blit(juego3,(640,20))
        juego4 = cargar_imagen("laberinto4.jpg")
        screen.blit(juego4,(40,300))
        juego5 = cargar_imagen("laberinto5.jpg")
        screen.blit(juego5,(340,300))
        juego6 = cargar_imagen("laberinto6.jpg")
        screen.blit(juego6,(640,300))
        # juego7 = cargar_imagen("laberinto7.jpg")
        # screen.blit(juego7,(75,370))
        # juego8 = cargar_imagen("laberinto8.jpg")
        # screen.blit(juego8,(375,370))
        # juego9 = cargar_imagen("laberinto9.jpg")
        # screen.blit(juego9,(675,370))
        # juego10 = cargar_imagen("laberinto10.jpg")
        # screen.blit(juego10,(75,545))
        
        
        #Efecto de sobreposicion del mouse sobre el laberinto
        #Laberinto1
        if 40 < mouse[0] < 40+220 and 20 < mouse[1] < 20+220:
            #Para crear el rectangulo (x-5,y-5,ancho+10,alto+10)
            pygame.draw.rect(screen, [255,214,192],(40-5,20-5,230,230))
            juego = cargar_imagen("laberinto2.jpg")
            screen.blit(juego1,(40,20))
            if click[0] == 1:
                return 1
        
        #Laberinto 2
        if 340 < mouse[0] < 340+220 and 20 < mouse[1] < 20+220:
            #Para crear el rectangulo (x-5,y-5,ancho+10,alto+10)
            pygame.draw.rect(screen, [255,214,192],(340-5,20-5,230,230))
            juego = cargar_imagen("laberinto2.jpg")
            screen.blit(juego,(340,20))
            if click[0] == 1:
                return 2
                
        #Laberinto3
        if 640 < mouse[0] < 640+220 and 20 < mouse[1] < 20+220:
            #Para crear el rectangulo (x-5,y-5,ancho+10,alto+10)
            pygame.draw.rect(screen, [255,214,192],(640-5,20-5,230,230))
            juego = cargar_imagen("laberinto3.jpg")
            screen.blit(juego,(640,20))
            if click[0] == 1:
                return 3
                
        #Laberinto4
        if 40 < mouse[0] < 40+220 and 300 < mouse[1] < 300+220:
            #Para crear el rectangulo (x-5,y-5,ancho+10,alto+10)
            pygame.draw.rect(screen, [255,214,192],(40-5,300-5,230,230))
            juego = cargar_imagen("laberinto4.jpg")
            screen.blit(juego,(40,300))
            if click[0] == 1:
                return 4
        
        #Laberinto5        
        if 340 < mouse[0] < 340+220 and 300 < mouse[1] < 300+220:
            #Para crear el rectangulo (x-5,y-5,ancho+10,alto+10)
            pygame.draw.rect(screen, [255,214,192],(340-5,300-5,230,230))
            juego = cargar_imagen("laberinto5.jpg")
            screen.blit(juego,(340,300))
            if click[0] == 1:
                return 5
                
        #Laberinto6
        if 640 < mouse[0] < 640+220 and 300 < mouse[1] < 300+220:
            #Para crear el rectangulo (x-5,y-5,ancho+10,alto+10)
            pygame.draw.rect(screen, [255,214,192],(640-5,300-5,230,230))
            juego = cargar_imagen("laberinto6.jpg")
            screen.blit(juego,(640,300))
            if click[0] == 1:
                return 6
                
        # #Laberinto7
        # if 75 < mouse[0] < 75+150 and 370 < mouse[1] < 370+148:
        #     #Para crear el rectangulo (x-5,y-5,ancho+10,alto+10)
        #     pygame.draw.rect(screen, [255,214,192],(75-5,370-5,160,158))
        #     juego = cargar_imagen("laberinto7.jpg")
        #     screen.blit(juego,(75,370))
        #     if click[0] == 1:
        #         return 7
        #
        # #Laberinto8
        # if 375 < mouse[0] < 375+150 and 370 < mouse[1] < 370+148:
        #     #Para crear el rectangulo (x-5,y-5,ancho+10,alto+10)
        #     pygame.draw.rect(screen, [255,214,192],(375-5,370-5,160,158))
        #     juego = cargar_imagen("laberinto8.jpg")
        #     screen.blit(juego,(375,370))
        #     if click[0] == 1:
        #         return 8
        #
        # #Laberinto9
        # if 675 < mouse[0] < 675+150 and 370 < mouse[1] < 370+148:
        #     #Para crear el rectangulo (x-5,y-5,ancho+10,alto+10)
        #     pygame.draw.rect(screen, [255,214,192],(675-5,370-5,160,158))
        #     juego = cargar_imagen("laberinto9.jpg")
        #     screen.blit(juego,(675,370))
        #     if click[0] == 1:
        #         return 9
        #
        # #Laberinto10
        # if 75 < mouse[0] < 75+150 and 545 < mouse[1] < 545+148:
        #     #Para crear el rectangulo (x-5,y-5,ancho+10,alto+10)
        #     pygame.draw.rect(screen, [255,214,192],(75-5,545-5,160,158))
        #     juego = cargar_imagen("laberinto10.jpg")
        #     screen.blit(juego,(75,545))
        #     if click[0] == 1:
        #         return 10
            
        if (375) < mouse[0] < (375 +170) and (600) < mouse[1] < (600 + 60):
            pygame.draw.rect(screen, [255,192,192],(375,600,170,60))
            if click[0] == 1:
                menu_intro()
        else:
            pygame.draw.rect(screen, [255,0,0] , (375,600,170,60))
        
        #letra - va luego
        smallText = pygame.font.SysFont("Arial",40)
        textSurf_jugar,textRect_jugar = text_objects_3("Regresar",smallText)
        textRect_jugar.center = (460,625)
        screen.blit(textSurf_jugar,textRect_jugar)    
        
        pygame.display.update()


# -- fin de Seleccion de definidos --------------------------------------------------------------------

# -- Inicio de Seleccion de Algoritmo --------------------------------------------------------------------

def menu_seleccion_algoritmo(intro):
    global banderaModoJuego
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        screen.fill([0,0,0])
        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        #Boton de DFS
        if (screen.get_width()*0.15) < mouse[0] < (screen.get_width()*0.15 +250) and (screen.get_height()*0.45) < mouse[1] < (screen.get_height()*0.45 + 60):
            pygame.draw.rect(screen, [215,194,7],(screen.get_width()*0.15,screen.get_height()*0.45,250,60))
            if click[0] == 1:
                banderaModoJuego = 0
        else:
            pygame.draw.rect(screen, [160,143,10] , (screen.get_width()*0.15,screen.get_height()*0.45,250,60))
        
        #Boton de BFS
        if (screen.get_width()*0.55) < mouse[0] < (screen.get_width()*0.55 +250) and (screen.get_height()*0.45) < mouse[1] < (screen.get_height()*0.45 + 60):
            pygame.draw.rect(screen, [31,233,200],(screen.get_width()*0.55,screen.get_height()*0.45,250,60))
            if click[0] == 1:
                banderaModoJuego = 1
        else:
            pygame.draw.rect(screen, [27,205,175] , (screen.get_width()*0.55 ,screen.get_height()*0.45,250,60))
            
        #Boton de A*
        if (screen.get_width()*0.35) < mouse[0] < (screen.get_width()*0.35 +250) and (screen.get_height()*0.60) < mouse[1] < (screen.get_height()*0.60 + 60):
            pygame.draw.rect(screen, [255,45,59],(screen.get_width()*0.35,screen.get_height()*0.60,250,60))
            if click[0] == 1:
                banderaModoJuego = 2
        else:
            pygame.draw.rect(screen, [145,28,29], (screen.get_width()*0.35 ,screen.get_height()*0.60,250,60))
            
        if banderaModoJuego == 0:
            pygame.draw.rect(screen, [215,194,7],(screen.get_width()*0.15,screen.get_height()*0.45,250,60))
        elif banderaModoJuego == 1:
            pygame.draw.rect(screen, [31,233,200],(screen.get_width()*0.55,screen.get_height()*0.45,250,60))
        elif banderaModoJuego == 2:
            pygame.draw.rect(screen, [255,45,59],(screen.get_width()*0.35,screen.get_height()*0.60,250,60))
            
        #Boton de Siguiente
        if (screen.get_width()*0.70) < mouse[0] < (screen.get_width()*0.70 +240) and (screen.get_height()*0.90) < mouse[1] < (screen.get_height()*0.90 + 50):
            pygame.draw.rect(screen, [192,255,192],(screen.get_width()*0.70,screen.get_height()*0.90,240,50))
            if click[0] == 1:
                quitarColor = 1
                valor = menu_seleccion_definidos(intro)
                juego(valor)
        else:
            pygame.draw.rect(screen, [0,255,0] , (screen.get_width()*0.70 ,screen.get_height()*0.90,240,50))
        
        #Palabras: BFS y DFS
        mediumText = pygame.font.SysFont("Arial",50)
        textSurf_jugar,textRect_jugar = text_objects_2("DFS",mediumText)
        textRect_jugar.center = (screen.get_width()*0.28,screen.get_height()*0.48)
        screen.blit(textSurf_jugar,textRect_jugar)
        
        textSurf_jugar,textRect_jugar = text_objects_2("BFS",mediumText)
        textRect_jugar.center = (screen.get_width()*0.68,screen.get_height()*0.48)
        screen.blit(textSurf_jugar,textRect_jugar)
        
        textSurf_jugar,textRect_jugar = text_objects_2("A *",mediumText)
        textRect_jugar.center = (screen.get_width()*0.49,screen.get_height()*0.64)
        screen.blit(textSurf_jugar,textRect_jugar)
        
        smallText = pygame.font.SysFont("Arial",40)
        textSurf_jugar,textRect_jugar = text_objects_2("Siguiente >>",smallText)
        textRect_jugar.center = (screen.get_width()*0.83,screen.get_height()*0.93)
        screen.blit(textSurf_jugar,textRect_jugar)
        
        pygame.display.update()


# -- Fin de Seleccion de Algoritmo --------------------------------------------------------------------

# -- Inicio de Seleccion de Juego --------------------------------------------------------------------

def menu_seleccion(intro):
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        screen.fill([0,0,0])
        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        #Boton de Aleatorio
        if (screen.get_width()*0.35) < mouse[0] < (screen.get_width()*0.35 +250) and (screen.get_height()*0.30) < mouse[1] < (screen.get_height()*0.30 + 60):
            pygame.draw.rect(screen, [255,214,192],(screen.get_width()*0.35,screen.get_height()*0.30,250,60))
            if click[0] == 1:
                juego(0)
        else:
            pygame.draw.rect(screen, [255,214,0] , (screen.get_width()*0.35,screen.get_height()*0.30,250,60))
            
        #Boton de definidos
        if (screen.get_width()*0.35) < mouse[0] < (screen.get_width()*0.35 +250) and (screen.get_height()*0.70) < mouse[1] < (screen.get_height()*0.70 + 60):
            pygame.draw.rect(screen, [244,125,192],(screen.get_width()*0.35,screen.get_height()*0.70,250,60))
            if click[0] == 1:
                menu_seleccion_algoritmo(intro)
                #valor = menu_seleccion_definidos(intro)
                #juego(valor)
        else:
            pygame.draw.rect(screen, [244,125,65] , (screen.get_width()*0.35,screen.get_height()*0.70,250,60))
        
        #Palabras: Definidos y Aleatorio
        mediumText = pygame.font.SysFont("Arial",40)
        textSurf_jugar,textRect_jugar = text_objects_2("Aleatorio",mediumText)
        textRect_jugar.center = (screen.get_width()*0.49,screen.get_height()*0.335)
        screen.blit(textSurf_jugar,textRect_jugar)
        
        textSurf_jugar,textRect_jugar = text_objects_2("Definido",mediumText)
        textRect_jugar.center = (screen.get_width()*0.49,screen.get_height()*0.735)
        screen.blit(textSurf_jugar,textRect_jugar)
        
        pygame.display.update()


# -- Fin de Seleccion de Juego --------------------------------------------------------------------

# -- Inicio de Menu -----------------------------------------------------------------------------------

def menu_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill([0,0,0])
        
        pacman_intro = cargar_imagen("intro_pacman.png")
        screen.blit(pacman_intro,(900/3,20))
        
        largeText = pygame.font.SysFont("Arial",70)
        TextSurf,TextRect = text_objects("PacMan",largeText)
        TextRect.center = (900/2, 320)
        screen.blit(TextSurf,TextRect)
        
        TextSurf,TextRect = text_objects("Artificial Intelligence",largeText)
        TextRect.center = (900/2, 400)
        screen.blit(TextSurf,TextRect) 
        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if (screen.get_width()*0.40) < mouse[0] < (screen.get_width()*0.40 +170) and (screen.get_height()*0.60) < mouse[1] < (screen.get_height()*0.60 + 60):
            pygame.draw.rect(screen, [192,255,192],(screen.get_width()*0.40,screen.get_height()*0.60,170,60))
            if click[0] == 1:
                #menu_seleccion(intro)
                menu_seleccion_algoritmo(intro)
        else:
            pygame.draw.rect(screen, [0,255,0] , (screen.get_width()*0.4,screen.get_height()*0.60,170,60))
            
        if (screen.get_width()*0.40) < mouse[0] < (screen.get_width()*0.40 +170) and (screen.get_height()*0.70) < mouse[1] < (screen.get_height()*0.70 + 60):
            pygame.draw.rect(screen, [255,192,192],(screen.get_width()*0.40,screen.get_height()*0.70,170,60))
            if click[0] == 1 :
                print "EXIT"
                pygame.quit()
                quit()
        else:
            pygame.draw.rect(screen, [255,0,0] , (screen.get_width()*0.40,screen.get_height()*0.70,170,60))
        
        smallText = pygame.font.SysFont("Arial",40)
        textSurf_jugar,textRect_jugar = text_objects_2("Jugar",smallText)
        textRect_jugar.center = (screen.get_width()*0.49,screen.get_height()*0.64)
        screen.blit(textSurf_jugar,textRect_jugar)
        
        textSurf_salir,textRect_salir = text_objects_2("Salir",smallText)
        textRect_salir.center = (screen.get_width()*0.49,screen.get_height()*0.74)
        screen.blit(textSurf_salir,textRect_salir)
        
        pygame.display.update()


# -- Fin de Menu ----------------------------------------------------------------------------------- 

if __name__ == "__main__":    
    #inicializamos pygame y la pantalla de juego
    pygame.init()
    Salir = False
    
    #Indicamos la dimension de la pantlla de juego
    window = pygame.display.set_mode([900,750])
    pygame.display.set_caption("pacman")  
    
    #creamos los sprites
    sprites = pygame.sprite.RenderUpdates()

    #Inicializamos la pantalla con fondo negro
    screen = pygame.display.get_surface()
    #screen.fill ([0,0,0])

    eventos = pygame.event.get()
    while Salir == False:
        menu_intro() 
    #--el juego ha finalizado