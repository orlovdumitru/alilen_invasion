from decouple import config


class Settings:
    """
    A class to store all settings for Alien Invasion.
    """
    def __init__(self) -> None:
        """
        Initialize the game's settings.
        """
        # self.screen_width = config("SCREEN_WIDTH", cast=int)
        # self.screen_height = config("SCREEN_HEIGHT", cast=int)
        self.bg_color = eval(config("BACKGROUND_COLOR"))
        self.clock_frame = config("CLOCK_FRAME", cast=int)
        self.ship_limit = config("SHIP_LIMIT", cast=int)
        self.ship_normal_size = config("SHIP_NORMAL_SIZE")
        self.ship_tiny_size = config("SHIP_TINY_SIZE")
        self.storage_path = config("STORAGE_PATH", cast=str)
        # Bullet settings
        self.bullet_width = config("BULLET_WIDTH", cast=int)
        self.bullet_height = config("BULLET_HEIGHT", cast=int)
        self.bullet_color = eval(config("BULLET_COLOR"))
        self.bullets_allowed = 10
        # set alien speed
        self.fleet_drop_speed = 10
        self.speedup_scale = 1.1
        # how quicly the alien point values increase
        self.score_scale = config("POINTS_INCREASE", cast=float)
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """
        Initialize settings that change throughout the game.
        """
        self.ship_speed = config("SHIP_SPEED", cast=int)
        self.bullet_speed = config("BULLET_SPEED", cast=float)
        self.alien_speed = 1.0
        self.alien_points = config("ALIEN_POINTS", cast=int)
        # fleet_direction of 1 represents right; -1 represents left
        self.alien_direction = {
            'right': 1,
            'left': -1,
            'direction': 'right'
        }

    def increase_speed(self):
        """
        Increase speed settings.
        """
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)