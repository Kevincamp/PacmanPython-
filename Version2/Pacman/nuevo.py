import pygame
import sys, copy, random, os, time
global segundos,contadorGalletas, contadorGalletasTotal
contadorGalletas = 0
contadorGalletasTotal = 0
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
        #print event
        if event.type == pygame.QUIT: 
            sys.exit(0) #se termina el programa
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print event.pos

# -- Fin de funciones Generales -------------------------------------------------------------
    
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
        global contadorGalletas
        v = 5
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
                #elif event.key == pygame.K_SPACE:
                #    if self.disparos > 0:
                #        if self.velocidad == [0,0]:
                #            bala = Bala (self, [3, 0])
                #        else:
                #            bala = Bala (self, [self.velocidad[0] * 3, self.velocidad[1] * 3])
                #        sprites.add ( bala )
                #        self.disparos -= 1
                    

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

def juego():
    global segundos
    global contadorGalletas
    global contadorGalletasTotal
    
    contadorGalletas = 0
    contadorGalletasTotal = 0
    
    Pared_x=0
    Salir = False
    Pared_y=0
    maze = Laberinto(15,15)
    laberinto = maze.getMaze()
    posicionSalida = maze.posicionSalida
    screen = pygame.display.get_surface()
    screen.fill((0,0,0))
    pygame.display.update()
    #creamos una copia de la pantalla para evitar su repintado completo cuando
    #se redibujen los sprites
    background = screen.copy()

    #bucle de redibujado de los screens
    reloj = pygame.time.Clock()
    for i in range(15):
            for j in range(15):  
                if(laberinto[i][j] == 1):
                    sprite = Pared ( "wall.png", [Pared_x,Pared_y], [50,50] )
                    sprites.add (sprite)
                    Pared_x+=50
                else:
                    if(i ==posicionSalida[0] and j==posicionSalida[1]):
                        sprite = MiSprite ("finish.png", [Pared_x, Pared_y])
                        pacman = Pacman("pacman.gif", [Pared_x,Pared_y])
                        sprites.add ( sprite )
                        sprites.add ( pacman )
                        Pared_x+=50
                        
                    else:
                        sprite = MiSprite ("bola.png", [Pared_x+10, Pared_y+10])
                        sprite.comestible = True
                        sprite.puntos = 5
                        sprites.add ( sprite )
                        Pared_x+=50
                        contadorGalletasTotal +=1
            Pared_x=0
            Pared_y+=50
      
    sonido_fondo = cargar_sonido ("sonido_fondo.wav").play(-1) #este sonido se repetira indefinidamente al indicar -1 como parametro   
    eventos = pygame.event.get()
    
    while Salir == False:
        segundos = pygame.time.get_ticks()/1000
        segundos = str(segundos)
        largeText = pygame.font.Font('./Fonts/BEBAS.TTF',20)
        TextSurf,TextRect = text_objects_3("Tiempo: ",largeText)
        TextRect.center = (805, 20)
        screen.blit(TextSurf,TextRect)
        TextSurf,TextRect = text_objects_3(segundos,largeText)
        TextRect.center = ((860), (20))
        screen.blit(TextSurf,TextRect)
        TextSurf,TextRect = text_objects_3("Galletas: ",largeText)
        TextRect.center = (805, 50)
        screen.blit(TextSurf,TextRect)
        #----------------------------Antes de presentar al contador hay que transformarlo a String-----------------------------
        #TextSurf,TextRect = text_objects_3(contadorGalletas,largeText)
        #TextRect.center = ((850), (30))
        #screen.blit(TextSurf,TextRect)
        
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

# -- Fin de Juego ------------------------------------------------------------------------------------

# -- Inicio de Menu -----------------------------------------------------------------------------------

def menu_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill([0,0,0])
        
        pacman_intro = cargar_imagen("intro_pacman.png")
        screen.blit(pacman_intro,(900/3,20))
        
        largeText = pygame.font.Font('./Fonts/PAC-FONT.TTF',30)
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
                juego()
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
        
        smallText = pygame.font.Font('./Fonts/BEBAS.TTF',40)
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
    window = pygame.display.set_mode([900,800])
    pygame.display.set_caption("pacman")  
    
    #creamos los sprites
    sprites = pygame.sprite.RenderUpdates()
    
    #Inicializamos la pantalla con fondo negro
    screen = pygame.display.get_surface()
    screen.fill ([0,0,0])
       
    eventos = pygame.event.get()
    while Salir == False:
        menu_intro() 
    #--el juego ha finalizado