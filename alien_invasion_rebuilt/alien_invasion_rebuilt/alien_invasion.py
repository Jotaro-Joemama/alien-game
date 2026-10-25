"""Run a small Alien Invasion game built with Pygame.

Controls:
    Left / Right arrows or A / D: move the ship
    Space: fire
    Q or Escape: quit
    R: restart after game over
"""

import sys
import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Manage the game window, player, alien fleet, and collisions."""

    def __init__(self):
        """Set up the game and create its initial objects."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.big_font = pygame.font.Font(None, 64)
        self.ship = Ship(self)
        self.bullets = Group()
        self.aliens = Group()
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.game_active = True
        self._create_fleet()

    def run_game(self):
        """Run the main game loop until the player quits."""
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(self.settings.frame_rate)

    def _check_events(self):
        """Respond to keyboard and window events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    self._quit_game()
                elif self.game_active and event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.ship.moving_right = True
                elif self.game_active and event.key in (pygame.K_LEFT, pygame.K_a):
                    self.ship.moving_left = True
                elif self.game_active and event.key == pygame.K_SPACE:
                    self._fire_bullet()
                elif not self.game_active and event.key == pygame.K_r:
                    self._restart_game()
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.ship.moving_right = False
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a bullet unless the allowed bullet limit is reached."""
        if len(self.bullets) < self.settings.bullets_allowed:
            self.bullets.add(Bullet(self))

    def _create_fleet(self):
        """Create enough rows of aliens to fill the upper screen area."""
        self.aliens.empty()
        sample = Alien(self)
        alien_width, alien_height = sample.rect.size
        available_width = self.settings.screen_width - 2 * alien_width
        aliens_per_row = max(1, available_width // (2 * alien_width))
        available_height = self.settings.screen_height - 150
        rows = max(1, min(5, available_height // (2 * alien_height)))

        for row_number in range(rows):
            for alien_number in range(aliens_per_row):
                alien = Alien(self)
                alien.x = alien_width + 2 * alien_width * alien_number
                alien.rect.x = round(alien.x)
                alien.rect.y = alien_height + 2 * alien_height * row_number
                self.aliens.add(alien)

    def _update_bullets(self):
        """Move bullets, remove off-screen bullets, and handle hits."""
        self.bullets.update()
        for bullet in list(self.bullets):
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # groupcollide removes each bullet and alien involved in a hit.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            self.score += 10 * sum(len(hit_aliens) for hit_aliens in collisions.values())
        if not self.aliens:
            self.bullets.empty()
            self.settings.alien_speed *= 1.15
            self._create_fleet()

    def _update_aliens(self):
        """Move the fleet, reverse it at edges, and check for collisions."""
        if any(alien.check_edges() for alien in self.aliens):
            self._change_fleet_direction()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        for alien in self.aliens:
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        """Drop every alien a little and reverse the fleet's direction."""
        for alien in self.aliens:
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Remove a ship life and reset the fleet, or end the game."""
        if self.ships_left > 1:
            self.ships_left -= 1
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.time.delay(350)
        else:
            self.ships_left = 0
            self.game_active = False

    def _restart_game(self):
        """Reset score, lives, speed, ship, and fleet after game over."""
        self.score = 0
        self.ships_left = self.settings.ship_limit
        self.settings.alien_speed = 1.0
        self.settings.fleet_direction = 1
        self.bullets.empty()
        self.ship.center_ship()
        self._create_fleet()
        self.game_active = True

    def _update_screen(self):
        """Draw the current game state and update the display."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets:
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        score_image = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        lives_image = self.font.render(f"Ships: {self.ships_left}", True, (255, 255, 255))
        self.screen.blit(score_image, (15, 12))
        self.screen.blit(lives_image, (15, 44))

        if not self.game_active:
            title = self.big_font.render("GAME OVER", True, (255, 100, 100))
            prompt = self.font.render("Press R to restart or Q to quit", True, (255, 255, 255))
            self.screen.blit(title, title.get_rect(center=self.screen.get_rect().center).move(0, -30))
            self.screen.blit(prompt, prompt.get_rect(center=self.screen.get_rect().center).move(0, 25))

        pygame.display.flip()

    @staticmethod
    def _quit_game():
        """Close Pygame and exit the program."""
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = AlienInvasion()
    game.run_game()
