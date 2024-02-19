import math
import pygame

class Bullet:
    def __init__(self, start_coords, angle, angle_offset, velocity, type):
        self.x, self.y = start_coords
        self.angle = angle
        self.angle_offset = angle_offset
        self.velocity = velocity * 100
        if type == 0:
            self.image = pygame.image.load("res/bullet.png")
        elif type == 1:
            self.image = pygame.image.load("res/long_bullet.png")
        elif type == 2:
            self.image = pygame.image.load("res/star_bullet.png")
        elif type == 3:
            self.image = pygame.image.load("res/sq_bullet.png")
        self.mask = pygame.mask.from_surface(self.image)
        self.a = 0
        self.original_rect = self.image.get_rect(center=(self.x, self.y))

    def update_and_display(self, screen, dt):
        self.angle = (self.angle + self.angle_offset) % 360

        self.cos_a = math.cos(math.radians(self.angle))
        self.sin_a = math.sin(math.radians(self.angle))

        self.x += (self.velocity * self.cos_a) * dt
        self.y += (self.velocity * self.sin_a) * dt

        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        rect_center = (self.x, self.y)
        self.rect = rotated_image.get_rect(center=rect_center)
        screen.blit(rotated_image, self.rect.topleft)
        #self.a = (self.a + 1) % 360

    def get_hitbox(self):
        new_width = int(0.25 * self.original_rect.width)
        new_height = int(0.25 * self.original_rect.height)

        smaller_rect = pygame.Rect(self.rect.centerx - (new_width / 2), self.rect.centery - (new_height / 2), new_width, new_height)

        return smaller_rect

class Player_Bullet():
    def __init__(self, coords, angle):
        self.x, self.y = coords
        self.velocity = 1000
        self.image = pygame.image.load("res/player_bullet.png")
        self.angle = 270 + angle
        self.a = 0
    
    def update_and_display(self, screen, dt):
        self.a = (self.a + (1 * dt)) % 360
        self.cos_a = math.cos(math.radians(self.angle))
        self.sin_a = math.sin(math.radians(self.angle))

        self.x += (self.velocity * self.cos_a) * dt
        self.y += (self.velocity * self.sin_a) * dt
        rotated_image = pygame.transform.rotate(self.image, -self.angle - self.a)
        rotated_image.set_alpha(128)
        rect_center = (self.x, self.y)
        self.rect = rotated_image.get_rect(center=rect_center)
        screen.blit(rotated_image, self.rect.topleft)

class Particle:
    def __init__(self, start_coords, angle, angle_offset, velocity, type):
        self.x, self.y = start_coords
        self.angle = angle
        self.angle_offset = angle_offset
        self.velocity = velocity * 100
        if type == 0:
            self.image = pygame.image.load("res/bullet.png")
        elif type == 1:
            self.image = pygame.image.load("res/long_bullet.png")
        elif type == 2:
            self.image = pygame.image.load("res/star_bullet.png")
        elif type == 3:
            self.image = pygame.image.load("res/sq_bullet.png")
        self.mask = pygame.mask.from_surface(self.image)
        self.a = 0
        self.original_rect = self.image.get_rect(center=(self.x, self.y))

    def update_and_display(self, screen, dt):
        self.angle = (self.angle + self.angle_offset) % 360

        self.cos_a = math.cos(math.radians(self.angle))
        self.sin_a = math.sin(math.radians(self.angle))

        self.x += (self.velocity * self.cos_a) * dt
        self.y += (self.velocity * self.sin_a) * dt

        rotated_image = pygame.transform.rotate(self.image, -self.angle - self.a)
        rect_center = (self.x, self.y)
        self.rect = rotated_image.get_rect(center=rect_center)
        screen.blit(rotated_image, self.rect.topleft)
        self.a = (self.a + 1) % 360