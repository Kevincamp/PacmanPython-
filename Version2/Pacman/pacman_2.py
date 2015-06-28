import pygame
import sys, copy, random, os

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
#--- Inicio Laberinto -------------------------------------------
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
    
        
        

#--- Fin Laberinto -------------------------------------------
          
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

         
#--- Inicio Pacman -----------------------------------------------            

class Pacman ( SpriteMovil ):
    NUMERO_FOTOGRAMAS = 8
    
    def __init__(self, fichero_imagen, pos_inicial):
        SpriteMovil.__init__(self, fichero_imagen, pos_inicial, [1,0]) 
        self.vidas = 3
        self.puntos = 0
        self.disparos = 2
        
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


    def update (self):
        #global eventos # explicitamente declaramos que "eventos" es una variable global
        global sprites 
        v = 1
        for event in eventos:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.velocidad[0] = -v
                    self.velocidad[1] = 0
                elif event.key == pygame.K_RIGHT:
                    self.velocidad[0] = v
                    self.velocidad[1] = 0
                elif event.key == pygame.K_UP:
                    self.velocidad[1] = -v
                    self.velocidad[0] = 0
                elif event.key == pygame.K_DOWN:
                    self.velocidad[1] = v
                    self.velocidad[0] = 0
                elif event.key == pygame.K_SPACE:
                    if self.disparos > 0:
                        if self.velocidad == [0,0]:
                            bala = Bala (self, [3, 0])
                        else:
                            bala = Bala (self, [self.velocidad[0] * 3, self.velocidad[1] * 3])
                        sprites.add ( bala )
                        self.disparos -= 1
                    

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
       
        if pygame.time.get_ticks() - self.__tiempoCambioFotograma > 100:
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
                        sprite.kill() # destruimos el sprite
                        #if hasattr ( sprite, "puntos" ):
                         #   self.puntos += sprite.puntos
                          #  informar ( self.rect.bottomright, "puntos %d" % (sprite.puntos) )
        

#--- Fin Pacman -----------------------------------------------            
        
#--- Inicio Pared ---------------------------------------------

class Pared ( MiSprite ):
    def __init__(self, color, pos_inicial, dimension):
        MiSprite.__init__(self)
    
        self.image = pygame.Surface(dimension) #creamos una superficie de las dimensiones indicadas
        self.image.fill(color)
            
        self.rect = self.image.get_rect()
        self.rect.topleft = pos_inicial
        self.infranqueable = True

    
    def update(self):
        MiSprite.update(self)

#--- Fin Pared ---------------------------------------------    

#--- Inicio marcador ---------------------------------------------    
  
class Marcador (MiSprite):
    def __init__(self, pacman):
        MiSprite.__init__(self)
        self.pacman = pacman
        self.font = pygame.font.SysFont("None", 20)
        self.rect = pygame.rect.Rect(0,0,0,0)

    
    def update(self):
        self.texto = "vidas: %d - puntos: %d - disparos: %d" % (self.pacman.vidas, self.pacman.puntos, self.pacman.disparos)
        self.image = self.font.render(self.texto, 1, (255, 255, 0))
        self.rect = self.image.get_rect()
        
        #situamos al marcador en la esquina inferior derecha
        self.rect.topleft = (pygame.display.get_surface().get_width() - self.rect.width, 
                     pygame.display.get_surface().get_height() - self.rect.height)
        
        MiSprite.update (self)

#--- Fin marcador ---------------------------------------------    

#--- Inicio Mensaje ---------------------------------------------    

class Mensaje (MiSprite):
    def __init__(self, texto, posicion = None, dim_font = 60, tiempo = 0 ):
        '''Muestra un mensaje en pantalla.
           Si indicamos un tiempo > 0, el mensaje desaparecera cuando transcurra dicho tiempo'''
        MiSprite.__init__(self)

        self.texto = texto
        self.font = pygame.font.SysFont("None", dim_font)
        self.image = self.font.render(self.texto, 1, (255, 255, 0))
        self.rect = self.image.get_rect()
        self.tiempo = tiempo
        if self.tiempo > 0:
            self.inicio = pygame.time.get_ticks()
        
        if posicion is None:
            posicion =[(pygame.display.get_surface().get_width() - self.rect.width ) / 2, 
                        (pygame.display.get_surface().get_height() - self.rect.height ) / 2 ]
        
        self.rect.topleft = posicion

    
    def update(self):
        MiSprite.update (self)
        if self.tiempo > 0 and pygame.time.get_ticks() - self.inicio > self.tiempo:
            self.kill()

#--- fin Mensaje ---------------------------------------------   
        
#--- funciones del modulo -------------------------------------

def ManejarEventos():
    global eventos # explicitamente declaramos que "eventos" es una variable global
    eventos = pygame.event.get()
    for event in eventos: 
        print event
        if event.type == pygame.QUIT: 
            sys.exit(0) #se termina el programa
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print event.pos

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


def kill(sprite):
    cargar_sonido("kill.wav").play()
    sprite.kill()
  
  
def game_over():
    '''El juego finaliza cuando no exista ningun pacman o fantasma'''
    existen_fantasmas = existen_pacman = False
    for sprite in sprites:
        if isinstance(sprite, Fantasma):
            existen_fantasmas = True
        elif isinstance (sprite, Pacman):
            existen_pacman = True
    
    return not ( existen_fantasmas and existen_pacman )
 
def informar ( posicion, texto ):
    mensaje = Mensaje ( texto, posicion, 20, 2000)
    sprites.add ( mensaje )
    
def text_objects(text, font):
    textSurface = font.render(text, True, [255,255,0])
    return textSurface, textSurface.get_rect()
    
def text_objects_2(text, font):
    textSurface = font.render(text, True, [0,0,0])
    return textSurface, textSurface.get_rect()

def menu_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill([0,0,0])
        
        largeText = pygame.font.Font('./Fonts/PAC-FONT.TTF',30)
        TextSurf,TextRect = text_objects("PacMan",largeText)
        TextRect.center = ((300/2), (300/5))
        screen.blit(TextSurf,TextRect)
        
        pacman_intro = cargar_imagen("intro_pacman.png")
        screen.blit(pacman_intro,(60/3,200/3))
        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if (screen.get_width()*0.30) < mouse[0] < (screen.get_width()*0.30 +130) and (screen.get_height()*0.80) < mouse[1] < (screen.get_height()*0.80 + 30):
            pygame.draw.rect(screen, [192,255,192],(screen.get_width()*0.30,screen.get_height()*0.80,130,30))
            if click[0] == 1:
               juego()
        else:
            pygame.draw.rect(screen, [0,255,0] , (screen.get_width()*0.30,screen.get_height()*0.80,130,30))
            
        if (screen.get_width()*0.30) < mouse[0] < (screen.get_width()*0.30 +130) and (screen.get_height()*0.90) < mouse[1] < (screen.get_height()*0.90 + 30):
            pygame.draw.rect(screen, [255,192,192],(screen.get_width()*0.30,screen.get_height()*0.90,130,30))
            if click[0] == 1 :
                print "EXIT"
                pygame.quit()
                quit()
        else:
            pygame.draw.rect(screen, [255,0,0] , (screen.get_width()*0.30,screen.get_height()*0.90,130,30))
            
       #pygame.draw.rect(screen, [255,0,0] , (screen.get_width()*0.30,screen.get_height()*0.90,130,30))
        
        smallText = pygame.font.Font('./Fonts/PAC-FONT.TTF',20)
        textSurf_jugar,textRect_jugar = text_objects_2("Jugar",smallText)
        textRect_jugar.center = (screen.get_width()*0.507,screen.get_height()*0.84)
        screen.blit(textSurf_jugar,textRect_jugar)
        
        textSurf_salir,textRect_salir = text_objects_2("Salir",smallText)
        textRect_salir.center = (screen.get_width()*0.507,screen.get_height()*0.94)
        screen.blit(textSurf_salir,textRect_salir)
        
        pygame.display.update()
        reloj.tick(15)   

def juego():
    Pared_x=0
    Salir = False
    Pared_y=0
    maze = Laberinto(15,20)
    laberinto = maze.getMaze()
    screen = pygame.display.get_surface()
    screen.fill ([0,0,0])
    
    #creamos una copia de la pantalla para evitar su repintado completo cuando
    #se redibujen los sprites
    background = screen.copy()

    #creamos los sprites
    sprites = pygame.sprite.RenderUpdates()  
    
    ubicado = 0
    for i in range(20):
            for j in range(15):
                if(i == 18 and ubicado == 0 and laberinto[i][j] == 0):
                        pacman = Pacman("pacman.gif", [Pared_x+2,Pared_y+2])
                        sprites.add ( pacman )
                        ubicado = 1
                    
                if(laberinto[i][j] == 1):
                    sprite = Pared ( [150,150,150], [Pared_x,Pared_y], [20,20] )
                    sprites.add (sprite)
                    Pared_x+=20
                else:
                    sprite = MiSprite ("bola.png", [Pared_x+2, Pared_y+2])
                    sprite.comestible = True
                    sprite.puntos = 5
                    sprites.add ( sprite )
                    Pared_x+=20
            Pared_x=0
            Pared_y+=20
            
    reloj = pygame.time.Clock() 
      
    sonido_fondo = cargar_sonido ("sonido_fondo.wav").play(-1) #este sonido se repetira indefinidamente al indicar -1 como parametro   
    eventos = pygame.event.get()
    #ManejarEventos ()
    while Salir == False:
        #eventos = pygame.event.get()
        ManejarEventos ()
        
        sprites.update ()
        sprites.clear (screen, background) 
        
        pygame.display.update (sprites.draw (screen))        
        
        reloj.tick (40) #tiempo de espera entre frames
    pygame.time.delay(2000) 
    #--el juego ha finalizado
    
    while True:
        eventos = pygame.event.get()
        ManejarEventos()
    

#--- Codigo de ejecucion inicial ------------------------------

if __name__ == "__main__":    
    #inicializamos pygame y la pantalla de juego
    pygame.init()
    Salir = False
    
    #Indicamos la dimension de la pantlla de juego
    window = pygame.display.set_mode([300,400])
    pygame.display.set_caption("pacman")  
    
    #Inicializamos la pantalla con fondo negro
    screen = pygame.display.get_surface()
    screen.fill ([0,0,0])

    #creamos los sprites
    sprites = pygame.sprite.RenderUpdates()  
    
    #bucle de redibujado de los screens
    reloj = pygame.time.Clock() 
       
    eventos = pygame.event.get()
    ManejarEventos ()
    while Salir == False:
        menu_intro()      
        
        #tiempo de espera entre frames
        reloj.tick (40) 
    
    #--el juego ha finalizado

            



