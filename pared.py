import pygame

class Pared(pygame.sprite.Sprite):
  def __init__(self,color,posini,dimension):
      pygame.sprite.Sprite.__init__(self)
      self.image = pygame.Surface(dimension)
      self.image.fill(color)
     
      self.rect = self.image.get_rect()
      self.rect.topleft = posini
      self.infranqueable = True

  def update(self):
      pygame.sprite.Sprite.update(self)