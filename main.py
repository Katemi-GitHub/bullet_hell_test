# project started 12/02/2024

import pygame
import sys
import math
from src.bullet import *
from src.player import *
from src.effects import *
from src.enemy import *
import base64
code = base64.b64encode(b"""
# uncomment this while compiling

pygame.init()

width, height = 500, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption("Polygon Hell")
pygame.display.set_icon(pygame.image.load("res/icon.png"))

player = Player(250, 500)
enemy = Enemy((250, 100))

bullets = []
particles = []
player_bullets = []
circles = []
i = 0
running = True
last_gen_time = 0
last_player_time = 0
circle = pygame.image.load("res/circle.png")
health = pygame.image.load("res/health_text.png")
heart = pygame.image.load("res/heart.png")
demo = pygame.image.load("res/demo.png")
circle.set_alpha(64)
previous_time = pygame.time.get_ticks()
enemy_dead = 0
temp = 0

while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((24, 24, 24))

    rotated_image = pygame.transform.rotate(circle, -i)
    rect = rotated_image.get_rect(center=(enemy.x, enemy.y))
    screen.blit(rotated_image, rect.topleft)

    i = i + (dt*100)

    player.display_player(screen, dt)

    if (player.health > 0) and (enemy.health > 0):
        bullets.extend(enemy.behaviour(dt, screen))
        player.move(dt)
        keys = pygame.key.get_pressed()
        current_time_player = pygame.time.get_ticks()
        if current_time_player - last_player_time >= 100:
            if keys[pygame.K_z]:
                player_bullets.append(Player_Bullet(player.rect.center, -30))
                player_bullets.append(Player_Bullet(player.rect.center, -10))
                player_bullets.append(Player_Bullet(player.rect.center, 10))
                player_bullets.append(Player_Bullet(player.rect.center, 30))
                last_player_time = current_time_player
            elif keys[pygame.K_x]:
                player_bullets.append(Player_Bullet(player.rect.center, -6))
                player_bullets.append(Player_Bullet(player.rect.center, -2))
                player_bullets.append(Player_Bullet(player.rect.center, 2))
                player_bullets.append(Player_Bullet(player.rect.center, 6))
                last_player_time = current_time_player
    if enemy.health < 1:
        if temp == 0:
            particles.extend(enemy.death())
            temp = 1
            enemy_dead = 1
    if player.health < 1:
        if temp == 0:
            particles.extend(player.death())
            temp = 1
    
    if enemy_dead == 1:
        screen.blit(demo, demo.get_rect(center=(width/2, height/2)))

    for player_bullet in player_bullets:
        player_bullet.update_and_display(screen, dt)
        if enemy.rect.colliderect(player_bullet.rect):
            player_bullets.remove(player_bullet)
            enemy.health -= 1

    for bullet in bullets:
        bullet.update_and_display(screen, dt)
        bullet_hitbox = bullet.get_hitbox()
        
        if player.rect.colliderect(bullet_hitbox) and player.i_frames < 1:
            bullets.remove(bullet)
            player.i_frames = 180
            player.health -= 1
    
    for particle in particles:
        particle.update_and_display(screen, dt)

    enemy.display(screen)

    player.display_hitbox(screen)

    screen.blit(health, health.get_rect(topleft=(10, 10)))

    for h in range(player.health):
        screen.blit(heart, heart.get_rect(topleft=(10 + h*26, 40)))

    if player.i_frames > 0:
        player.i_frames -= dt*100
    elif player.i_frames < 0:
        player.i_frames = 0

    bullets = [bullet for bullet in bullets if 0 <= bullet.x <= width and 0 <= bullet.y <= height]
    particles = [particle for particle in particles if 0 <= particle.x <= width and 0 <= particle.y <= height]
    player_bullets = [player_bullet for player_bullet in player_bullets if 0 <= player_bullet.x <= width and 0 <= player_bullet.y <= height]

    pygame.display.flip()

pygame.quit()
sys.exit()

""")
exec(base64.b64decode(code))