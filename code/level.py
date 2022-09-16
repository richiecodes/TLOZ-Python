import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice

PLAYER_START_POS = (1300, 2000)

# TODO: ADD WEAPONS

class Level:
  def __init__(self):
    self.display_surface = pygame.display.get_surface()
    self.visible_sprites = YSortCameraGroup()
    self.obstacle_sprites = pygame.sprite.Group()

    self.create_map()

  def create_map(self):
    layout = {
      'boundary': import_csv_layout('./map/map_FloorBlocks.csv'),
      'grass': import_csv_layout('./map/map_Grass.csv'),
      'object': import_csv_layout('./map/map_Objects.csv'),
    }

    graphics = {
      'grass': import_folder('./graphics/grass'),
      'object': import_folder('./graphics/objects')
    }

    for style, layout in layout.items():
      for row_index, row in enumerate(layout):
        for col_index, col in enumerate(row):
          if col != '-1':
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            if style == 'boundary':
              Tile((x,y), [self.obstacle_sprites], 'invisible')
            if style == 'grass':
              random_image = choice(graphics['grass'])
              Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'grass', random_image)
            if style == 'object':
              surf = graphics['object'][int(col)]
              Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)

    self.player = Player(PLAYER_START_POS, [self.visible_sprites], self.obstacle_sprites)

  def run(self):
    self.visible_sprites.custom_draw(self.player)
    self.visible_sprites.update()
    debug('|--**DEBUG**--|')
    debug(f'Pos: (x: {self.player.rect.centerx}, y: {self.player.rect.centery})', x=10, y=33)
    debug(f'State: {self.player.status}', x=10,y=56)


class YSortCameraGroup(pygame.sprite.Group):
  def __init__(self):
    super().__init__()
    self.display_surface = pygame.display.get_surface()
    self.half_width = self.display_surface.get_size()[0] // 2
    self.half_height = self.display_surface.get_size()[1] // 2

    self.offset = pygame.math.Vector2()

    self.floor_surface = pygame.image.load('./graphics/tilemap/ground.png').convert()
    self.floor_rect = self.floor_surface.get_rect(topleft=(0,0))

  def custom_draw(self, player):
    
    self.offset.x = player.rect.centerx - self.half_width
    self.offset.y = player.rect.centery - self.half_height

    floor_offset_pos = self.floor_rect.topleft - self.offset
    self.display_surface.blit(self.floor_surface, floor_offset_pos)

    for sprite in sorted(self.sprites(), key= lambda sprite: sprite.rect.centery):
      offset_pos = sprite.rect.topleft - self.offset
      self.display_surface.blit(sprite.image, offset_pos)