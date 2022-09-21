import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        direction = player.status.split('_')[0]

        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect(center = player.rect.center)

        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0, 16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midleft = player.rect.midleft + pygame.math.Vector2(0, 16))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midright + pygame.math.Vector2(0, 16))
        else:
            self.rect = self.image.get_rect(midbottom = player.rect.center)