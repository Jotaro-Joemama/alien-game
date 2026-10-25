"""Store the settings used by the Alien Invasion game."""


class Settings:
    """Keep game settings in one place so they are easy to adjust."""

    def __init__(self):
        """Initialize settings that do not change while the game runs."""
        self.screen_width = 1000
        self.screen_height = 700
        self.bg_color = (12, 18, 38)
        self.frame_rate = 60

        self.ship_speed = 5.0
        self.ship_limit = 3

        self.bullet_speed = 8.0
        self.bullet_width = 5
        self.bullet_height = 16
        self.bullet_color = (255, 220, 90)
        self.bullets_allowed = 4

        self.alien_speed = 1.0
        self.fleet_drop_speed = 22
        # 1 means move right; -1 means move left.
        self.fleet_direction = 1
