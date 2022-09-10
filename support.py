from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

def import_folder(path):
    img_list = []
    for _,_,imgFiles in walk(path):
        for img in imgFiles:
            full_path = path + '/' + img
            image = pygame.image.load(full_path).convert_alpha()
            img_list.append(image)
    return img_list