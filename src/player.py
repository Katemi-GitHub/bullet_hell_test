import pygame
import math
from src.bullet import *

class Player:
    def __init__(self, x, y):
        self.player_image = pygame.image.load("res/placeholder.png")
        self.hitbox_image = pygame.image.load("res/player.png")
        self.rect = pygame.Rect(x, y, self.hitbox_image.get_width(), self.hitbox_image.get_height())
        self.mask = pygame.mask.from_surface(self.hitbox_image)
        self.i_frames = 0
        self.speed = 150
        self.health = 5
        self.flicker_timer = 0
        self.flicker_interval = 0.1
    
    def move(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed * dt, 0)
        elif keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed * dt, 0)

        if keys[pygame.K_UP]:
            self.rect.move_ip(0, -self.speed * dt)
        elif keys[pygame.K_DOWN]:
            self.rect.move_ip(0, self.speed * dt)

    def display_player(self, screen, dt):
        self.player_image.set_alpha(128)
        offset_x = (self.hitbox_image.get_width() - self.player_image.get_width()) // 2
        offset_y = (self.hitbox_image.get_height() - self.player_image.get_height()) // 2

        if self.i_frames > 0:
            self.flicker_timer += dt
            if self.flicker_timer >= self.flicker_interval:
                self.flicker_timer = 0
                self.player_image.set_alpha(128 if self.player_image.get_alpha() == 0 else 0)
                self.i_frames -= 1

        screen.blit(self.player_image, (self.rect.x + offset_x, self.rect.y + offset_y))
    
    def display_hitbox(self, screen):
        screen.blit(self.hitbox_image, self.rect.topleft)
    
    def death(self):
        bullets = []
        for i in range(15):
            bullets.append(Particle((self.x, self.y), i * 24, 0, 3, 3))
        return bullets