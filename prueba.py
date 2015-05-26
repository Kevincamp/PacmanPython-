#Modulos
import pygame
from pygame.locals import *

#Constantes
WIDTH = 640
HEIGHT = 480

#Clases -----------------------------------------
class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("images/PacMan.png",True)
        self.size = self.image.get_size()
        self.small_img = pygame.transform.scale(self.image,(int(self.size[0]/4),int(self.size[1]/4)))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.centery = HEIGHT/2
        self.speed = [0.5, -0.5]
            

#Funciones ----------------------------------------
def load_image(filename, transparent = False):
    try: image = pygame.image.load(filename)
    except pygame.error,message:
        raise SystemExit, message
    image = image.convert()
    if transparent:
        color =  image.get_at((0,0))
        image.set_colorkey(color,RLEACCEL)
    return image
    
#---------------------------------------------------
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    background = pygame.Surface(screen.get_size())
    background.fill((0,0,0))
    pygame.display.set_caption("PacMan")
    pygame.mouse.set_visible(0)
    
    pacman = Pacman()
    clock = pygame.time.Clock()
    
    while True:
        time = clock.tick(60)
        keys = pygame.key.get_pressed()
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)
            
            #pacman.mover(time,keys)   
            screen.blit(background,(0,0))
            screen.blit(pacman.small_img, pacman.rect)
            pygame.display.flip()
    return 0


if __name__=='__main__':
    pygame.init()
    main()