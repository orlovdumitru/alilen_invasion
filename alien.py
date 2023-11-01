import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """
    A class to represent aliens.
    """

    def __init__(self, ai_game) -> None:
        super().__init__()
        self.screen = ai_game.screen
        self.settings= ai_game.settings
        # load the alien image and set it rect attribure.
        self.image = pygame.image.load("images/spaceship_small.bmp")
        self.rect = self.image.get_rect()
        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # Store the anien's exact horizontal position.
        self.x = float(self.rect.x)
        
    def update(self):
        """
        Move the alien to the right/left.
        """
        al_direction = self.settings.alien_direction
        self.x += self.settings.alien_speed * al_direction[al_direction['direction']] # 1 or -1 
        print(self.settings.alien_speed * al_direction[al_direction['direction']])
        self.rect.x = self.x

    def check_edges(self):
        """
        Return True if alien is at edge of screen.
        """
        screen_rect = self.screen.get_rect()
        if self.rect.right > screen_rect.right:
            return 'left'
        elif self.rect.left <= 0:
            return 'right'
        return None