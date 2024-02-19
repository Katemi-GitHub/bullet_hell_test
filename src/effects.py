import pygame
import math

class MenacingCircle:
    def __init__(self, screen, name):
        self.screen = screen
        self.circle_image = pygame.image.load("res/menacing_circle.png")
        if name == "spell_vortex":
            self.above_image = pygame.image.load("res/spell_vortex.png")
        elif name == "WALL":
            self.above_image = pygame.image.load("res/WALL.png")
        self.angle = 0
        self.scale = 1
        self.alpha = 255
        self.active = True

    def draw(self, center):
        if not self.active:
            return

        # Update the alpha value for both images
        self.alpha -= 4
        self.alpha = max(0, self.alpha)

        # Draw the menacing circle
        rotated_image = pygame.transform.rotate(self.circle_image, self.angle)
        rect = rotated_image.get_rect(center=center)
        scaled_image = pygame.transform.scale(rotated_image, (int(rect.width * self.scale), int(rect.height * self.scale)))
        alpha_surface = pygame.Surface(scaled_image.get_size(), pygame.SRCALPHA)
        alpha_surface.fill((255, 255, 255, self.alpha))
        scaled_image.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        adjusted_topleft = (rect.topleft[0] - (scaled_image.get_width() - rect.width) / 2,
                            rect.topleft[1] - (scaled_image.get_height() - rect.height) / 2)

        self.screen.blit(scaled_image, adjusted_topleft)

        # Draw the above image centered on the menacing circle
        above_rect = self.above_image.get_rect(center=center)
        above_rect.topleft = (adjusted_topleft[0] + (scaled_image.get_width() - above_rect.width) / 2,
                              adjusted_topleft[1] + (scaled_image.get_height() - above_rect.height) / 2)
        self.above_image.set_alpha(self.alpha)
        self.screen.blit(self.above_image, above_rect.topleft)
        
        self.scale += 0.05
        self.angle += 1
    
        if self.alpha <= 0:
            self.active = False

# Rest of your code remains unchanged
