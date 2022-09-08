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
        self.visable_sprite = pygame.sprite.Group()
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
        self.visable_sprite.draw(self.display_surface)
        self.visable_sprite.update()
        debug(self.player.direction)