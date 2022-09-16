import pygame, sys
from settings import *
from level import Level

class Game:
  def __init__(self):
    pygame.init()
    self.window = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT)) #pygame.FULLSCREEN)
    pygame.display.set_caption('Zelda')

    self.level = Level()

  def run(self):
    clock = pygame.time.Clock()
    while (True):
      
      for e in pygame.event.get():
        if e.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if e.type == pygame.KEYDOWN:
          if e.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
          if e.key == pygame.K_f:
            pygame.display.toggle_fullscreen()

      self.window.fill('#71DDEE')
      self.level.run()
      clock.tick(FPS)
      pygame.display.update()


if __name__ == '__main__':
  g = Game()
  g.run()