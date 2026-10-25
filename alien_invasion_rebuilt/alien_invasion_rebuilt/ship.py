"""Define the player's ship."""

from pathlib import Path
import pygame


class Ship(pygame.sprite.Sprite):
    """Represent the ship controlled by the player."""

    def __init__(self, game):
        """Create the ship and place it near the bottom of the screen."""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        image_path = Path(__file__).parent / "Assets" / "images" / "ship.png"
        try:
            self.image = pygame.image.load(str(image_path)).convert_alpha()
            self.image = pygame.transform.smoothscale(self.image, (64, 44))
        except (pygame.error, FileNotFoundError):
            self.image = pygame.Surface((64, 44), pygame.SRCALPHA)
            pygame.draw.polygon(
                self.image, (90, 220, 255),
                [(32, 0), (61, 39), (32, 30), (3, 39)]
            )
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()
        self.rect.midbottom = (self.screen_rect.centerx, self.screen_rect.bottom - 18)
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Move the ship while keeping it inside the screen."""
        if self.moving_right:
            self.x += self.settings.ship_speed
        if self.moving_left:
            self.x -= self.settings.ship_speed
        max_x = self.screen_rect.right - self.rect.width
        self.x = max(0, min(self.x, max_x))
        self.rect.x = round(self.x)

    def center_ship(self):
        """Move the ship back to the bottom-center after a collision."""
        self.rect.midbottom = (self.screen_rect.centerx, self.screen_rect.bottom - 18)
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the ship on the screen."""
        self.screen.blit(self.image, self.rect)
