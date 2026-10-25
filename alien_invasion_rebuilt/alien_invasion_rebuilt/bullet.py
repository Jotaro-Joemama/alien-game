"""Define bullets fired by the player's ship."""

import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Represent a small projectile that travels upward."""

    def __init__(self, game):
        """Create a bullet at the top-center of the player's ship."""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet upward."""
        self.y -= self.settings.bullet_speed
        self.rect.y = round(self.y)

    def draw_bullet(self):
        """Draw the bullet as a colored rectangle."""
        pygame.draw.rect(self.screen, self.settings.bullet_color, self.rect)
