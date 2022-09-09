import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug

class Level:
    def __init__(self) -> None:
        
        #gets display surface from anywhere in the code
        self.display_surface = pygame.display.get_surface()

        #set up sprites for obstacles
        self.visable_sprite = YSortCameraGroup()
        self.obstacle_sprite = pygame.sprite.Group()
        self.create_map()

    def create_map(self):
        for i, row in enumerate(MAP):
            for j, col in enumerate(row):
                x = j*TILESIZE
                y = i*TILESIZE
                if col == 'x':
                    Tile((x,y), [self.visable_sprite, self.obstacle_sprite])
                if col == 'p':
                    self.player = Player((x,y), [self.visable_sprite], self.obstacle_sprite)

    def run(self):
        self.visable_sprite.custom_draw(self.player)
        self.visable_sprite.update()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]//2
        self.half_height = self.display_surface.get_size()[1]//2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):

        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in sorted(self.sprites(), key=lambda sprite:sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)