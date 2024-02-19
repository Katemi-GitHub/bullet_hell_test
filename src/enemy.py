import pygame
import math
import random
from src.bullet import *
from src.effects import *

class Enemy():
    def __init__(self, coords):
        self.x, self.y = coords
        self.image = pygame.image.load("res/enemy.png")
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.idle_timer = 3
        self.state = "idle"
        self.attack_state = "None"
        self.attack_pattern = 0
        self.temp_rot = 0
        self.cycles = 0
        self.last_time = 0
        self.circles = []
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = 0.5
        self.health = 1000
    
    def move_to_random_place(self):
        target_x = random.randint(25, 475)
        target_y = random.randint(25, 175)
        distance_x = target_x - self.x
        distance_y = target_y - self.y
        magnitude = math.sqrt(distance_x**2 + distance_y**2)
        self.velocity_x = (distance_x / magnitude) * self.acceleration
        self.velocity_y = (distance_y / magnitude) * self.acceleration

    def move(self, dt):
        self.x += self.velocity_x * (dt*100)
        self.y += self.velocity_y * (dt*100)

    def pattern_spiral(self):
        bullets = []
        self.temp_rot += 1
        self.cycles -= 1

        bullets.append(Bullet((self.x, self.y),       self.temp_rot * 11, 0.1, 2, 1))
        bullets.append(Bullet((self.x, self.y), 120 + self.temp_rot * 11, 0.2, 2, 1))
        bullets.append(Bullet((self.x, self.y), 240 + self.temp_rot * 11, 0.3, 2, 1))

        return bullets

    def pattern_star(self):
        bullets = []
        self.cycles -= 1
        self.temp_rot += 4.5
        for i in range(80):
            temp = abs(math.sin(5 * (i*9) * (math.pi/360))) * 0.66
            bullets.append(Bullet((self.x, self.y), i * 9 + self.temp_rot, -0.25, 2 - temp, 2))
        return bullets

    def pattern_flower(self):
        bullets = []
        self.cycles -= 1
        self.temp_rot += 4.5
        for i in range(80):
            temp = abs(math.sin(5 * (i*9) * (math.pi/360))) * 0.66
            bullets.append(Bullet((self.x, self.y), i * 9 + self.temp_rot, -0.25, 2 + temp, 2))
        return bullets
    
    def pattern_WALL(self):
        bullets = []
        self.cycles -= 1
        for i in range(120):
            bullets.append(Bullet((self.x, self.y), i*3, 0, 2, 1))
        return bullets

    def pattern_spiral_hardest(self):
        bullets = []
        self.temp_rot += 1
        self.cycles -= 1

        for i in range(3):
            bullets.append(Bullet((self.x, self.y),         self.temp_rot * 10, 0, 3 - (i*0.25), 0))
            bullets.append(Bullet((self.x, self.y), 120 +   self.temp_rot * 10, 0, 3 - (i*0.25), 0))
            bullets.append(Bullet((self.x, self.y), 240 +   self.temp_rot * 10, 0, 3 - (i*0.25), 0))
            bullets.append(Bullet((self.x, self.y),  5  -   self.temp_rot * 10, 0, 3 - (i*0.25), 3))
            bullets.append(Bullet((self.x, self.y), 125 -   self.temp_rot * 10, 0, 3 - (i*0.25), 3))
            bullets.append(Bullet((self.x, self.y), 245 -   self.temp_rot * 10, 0, 3 - (i*0.25), 3))

        return bullets

    def behaviour(self, dt, screen):
        if self.state == "idle":
            if self.idle_timer < 1:
                self.state = "move"
                self.idle_timer = 2
                return []
            else:
                self.idle_timer += (-1) * dt
            return []
        
        if self.state == "move":
            self.move_to_random_place()
            self.state = "moving"
            return []

        if self.state == "moving":
            if self.idle_timer < 1:
                self.state = "attack"
                return []
            else:
                self.idle_timer += (-1) * dt
                self.move(dt)
                return []
        
        if self.state == "attack":
            if self.attack_state == "None":
                self.temp_rot = 0
                self.attack_pattern = random.randint(1, 5)
                self.attack_state = "Midway"

            if self.attack_pattern == 1:
                if self.attack_state == "Midway":
                    self.cycles = 180
                    self.attack_state = "Executing"
                if self.cycles < 1:
                    self.attack_state = "None"
                    self.state = "idle"
                    self.idle_timer = 3
                    return []
                else:
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_time >= 50:
                        self.last_time = current_time
                        return self.pattern_spiral()
        
            if self.attack_pattern == 2:
                if self.attack_state == "Midway":
                    self.cycles = 5
                    self.attack_state = "Executing"
                if self.cycles < 1:
                    self.attack_state = "None"
                    self.state = "idle"
                    self.idle_timer = 3
                    return []
                else:
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_time >= 500:
                        self.last_time = current_time
                        return self.pattern_star()
        
            elif self.attack_pattern == 3:
                if self.attack_state == "Midway":
                    self.circles.append(MenacingCircle(screen, "spell_vortex"))
                    self.cycles = 90
                    self.attack_state = "Executing"
                if self.cycles < 1:
                    self.attack_state = "None"
                    self.state = "idle"
                    self.idle_timer = 3
                    return []
                else:
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_time >= 50:
                        self.last_time = current_time
                        return self.pattern_spiral_hardest()
            
            if self.attack_pattern == 4:
                if self.attack_state == "Midway":
                    self.cycles = 5
                    self.attack_state = "Executing"
                if self.cycles < 1:
                    self.attack_state = "None"
                    self.state = "idle"
                    self.idle_timer = 3
                    return []
                else:
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_time >= 500:
                        self.last_time = current_time
                        return self.pattern_flower()
            
            if self.attack_pattern == 5:
                if self.attack_state == "Midway":
                    self.circles.append(MenacingCircle(screen, "WALL"))
                    self.cycles = 1
                    self.attack_state = "Executing"
                if self.cycles < 1:
                    self.attack_state = "None"
                    self.state = "idle"
                    self.idle_timer = 3
                    return []
                else:
                    return self.pattern_WALL()
            
        return []
    
    def display(self, screen):
        self.rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, self.rect.topleft)
        for m_circle in self.circles:
            m_circle.draw((250, 125))
            if m_circle.alpha == 0:
                self.circles.remove(m_circle)
    
    def death(self):
        bullets = []
        for i in range(15):
            bullets.append(Particle((self.x, self.y), i * 24, 0.5, 3, 2))
        return bullets