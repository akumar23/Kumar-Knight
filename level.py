import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice

class Level:
    def __init__(self) -> None:
        
        #gets display surface from anywhere in the code
        self.display_surface = pygame.display.get_surface()

        #set up sprites for obstacles
        self.visable_sprite = YSortCameraGroup()
        self.obstacle_sprite = pygame.sprite.Group()
        self.create_map()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_Objects.csv')
        }
        
        graphics = {
            'grass' : import_folder('graphics/Grass')
        }

        for style, layout in layouts.items():
            for i, row in enumerate(layout):
                for j, col in enumerate(row):
                    if col != '-1':
                        x = j*TILESIZE
                        y = i*TILESIZE
                        if style == 'boundary':
                            Tile((x,y), [self.obstacle_sprite], 'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x,y), [self.visable_sprite, self.obstacle_sprite], 'grass', random_grass_image)

                        if style == 'object':
                            pass
                    """
                    if col == 'x':
                        Tile((x,y), [self.visable_sprite, self.obstacle_sprite])
                    if col == 'p':
                        self.player = Player((x,y), [self.visable_sprite], self.obstacle_sprite)
                    """
        
        self.player = Player((2000, 1430), [self.visable_sprite], self.obstacle_sprite)

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

        self.floor_surf = pygame.image.load('graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))    

    def custom_draw(self, player):

        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite:sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)