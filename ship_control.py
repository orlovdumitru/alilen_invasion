import pygame
from config.settings import Settings


class ShipControl:
    """
    Class to control the ship.
    """
    move_r = False
    move_l = False

    def __init__(self) -> None:
        """
        Initialize ship controler.
        """
        # self.settings = Settings()
        # self.game = ai_game
        pass

    def control_ship(self, event):
        """
        Controling Ship.
        """
        if event.type == pygame.KEYDOWN:
            self._key_down(event)            
        if event.type == pygame.KEYUP:
            self._key_up(event)

    def _key_down(self, event):
        """
        All key down events.
        """
        if event.key == pygame.K_RIGHT:
            self.move_r = True
        elif event.key == pygame.K_LEFT:
            self.move_l = True

    def _key_up(self, event):
        """
        All key up events.
        """
        if event.key == pygame.K_RIGHT:
            self.move_r = False
        elif event.key == pygame.K_LEFT:
            self.move_l = False
            
    def update_sip_position(self):
        """
        Update ship position on every iteration run game.
        """
        if self.ship.rect.x < self.settings.screen_width - 100 and self.move_r:
            self.move_right
        elif self.ship.rect.x > 0 and self.move_l:
            self.move_left

    @property
    def move_left(self):
        """
        Move ship to the left.
        """
        self.ship.rect.x -= self.settings.ship_speed

    @property
    def move_right(self):
        """
        Move ship to the right.
        """
        self.ship.rect.x += self.settings.ship_speed
  