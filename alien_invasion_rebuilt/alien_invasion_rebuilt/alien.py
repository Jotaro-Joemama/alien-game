"""Define an alien and its fleet movement."""

from pathlib import Path
import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Represent one alien in the fleet."""

    def __init__(self, game):
        """Load the alien image and place it initially at the top-left."""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        image_path = Path(__file__).parent / "Assets" / "images" / "enemy_4.png"
        try:
            self.image = pygame.image.load(str(image_path)).convert_alpha()
            self.image = pygame.transform.scale(self.image, (42, 42))
        except (pygame.error, FileNotFoundError):
            self.image = pygame.Surface((42, 42), pygame.SRCALPHA)
            pygame.draw.ellipse(self.image, (110, 255, 120), self.image.get_rect())
            pygame.draw.circle(self.image, (20, 35, 20), (13, 16), 4)
            pygame.draw.circle(self.image, (20, 35, 20), (29, 16), 4)
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def update(self):
        """Move the alien horizontally with the rest of the fleet."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = round(self.x)

    def check_edges(self):
        """Return True when this alien touches either horizontal edge."""
        screen_rect = self.screen.get_rect()
        if self.settings.fleet_direction == 1:
            return self.rect.right >= screen_rect.right
        return self.rect.left <= 0
