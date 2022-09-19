import pygame
from settings import *
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, create_attack) -> None:
        super().__init__(groups)
        self.image = pygame.image.load('graphics/batman.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))

        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -26)

        self.import_player_assests()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15

        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.attackCooldown = 400
        self.attackTimer = None
        self.obstacle_sprites = obstacle_sprites

        self.create_attack = create_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        print(self.weapon)


    def import_player_assests(self):
        character_path = 'graphics/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
            'right_idle': [], 'left_idle': [], 'up_idle':[], 'down_idle': [],
            'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}
        
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
            self.status = "up"
            self.image = pygame.image.load('graphics/player/up_idle/idle_up.png').convert_alpha()            
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
            self.status = "down"
            self.image = pygame.image.load('graphics/player/down_idle/idle_down.png').convert_alpha()           
        else:
            self.direction.y = 0
            self.status = "down_idle"
            self.image = pygame.image.load('graphics/batman.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (64, 64))             

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.status = "right"
            self.image = pygame.image.load('graphics/player/right_idle/idle_right.png').convert_alpha()
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.image = pygame.image.load('graphics/player/left_idle/idle_left.png').convert_alpha()            
            self.status = "left"
        else:
            self.direction.x = 0
            self.status = "right_idle"
            self.image = pygame.image.load('graphics/batman.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (64, 64))           

        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attackTimer = pygame.time.get_ticks()
            self.status = "right_attack"
            self.create_attack()
        
        if keys[pygame.K_LCTRL] and not self.attacking:
            self.attacking = True
            self.attackTimer = pygame.time.get_ticks()
            self.status = "right_attack"
            print('magic')
    
    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right 

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldown(self):
        time = pygame.time.get_ticks()
        if self.attacking:
            if time - self.attackTimer >= self.attackCooldown:
                self.attacking = False

    def update(self):
        self.input()
        self.cooldown()
        self.move(self.speed)