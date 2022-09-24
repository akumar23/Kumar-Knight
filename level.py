import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice
from weapon import Weapon


class Level:
    def __init__(self) -> None:
        
        #gets display surface from anywhere in the code
        self.display_surface = pygame.display.get_surface()

        #set up sprites for obstacles
        self.visable_sprite = YSortCameraGroup()
        self.obstacle_sprite = pygame.sprite.Group()

        self.current_attack = None

        self.create_map()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_Objects.csv')
        }
        
        graphics = {
            'grass' : import_folder('graphics/Grass'),
            'objects' : import_folder('graphics/objects')
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
                            if (int(col) < len(graphics['objects'])):
                                surf = graphics['objects'][int(col)]
                                Tile((x,y), [self.visable_sprite, self.obstacle_sprite], 'object', surf)
        
        self.player = Player((2000, 1430), [self.visable_sprite], self.obstacle_sprite, self.create_attack, self.destroy_weapon)

    def create_attack(self):
        self.current_attack = Weapon(self.player[self.visable_sprite])
    
    def destroy_weapon(self):
        if self.current_attack:
            self.current_attack.kill()
        self.create_attack = None

    def create_attack(self):
        Weapon(self.player, [self.visable_sprite])

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