import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """
    A class to manage the ship.
    """
    def __init__(self, ai_game, ship_path='media/images/small_titan_ship_2.bmp') -> None:
        """
        Initialize the ship and set its starting position.
        """
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        # load ship image and get its rect.
        self.image = pygame.image.load(ship_path)
        self.rect = self.image.get_rect()
        # start each newe ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """
        Draw the ship at its current location.
        """
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """
        Center the ship on the screen.
        """
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
    