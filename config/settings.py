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
        self.ship_speed = config("SHIP_SPEED", cast=int)
        # Bullet settings
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 10
        # set alien speed
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left
        self.alien_direction = {
            'right': 1,
            'left': -1,
            'direction': 'right'
        }
