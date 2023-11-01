import sys
import pygame

from config.settings import Settings
from bullet import Bullet
from ship import Ship
from ship_control import ShipControl
from alien import Alien


class AlienInvasion(ShipControl):
    """
    Manage game assets and behavor.
    """

    def __init__(self) -> None:
        """
        Initialize the game, create game resources.
        """
        pygame.init()
        self.settings = Settings()
        # screen size control (full screen)
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height - 70
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # define frame rate (clock) to run the same on all systems
        self.clock = pygame.time.Clock()
        # window title
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()


    def run_game(self):
        """
        Start the main loop for the game.
        """
        while True:
            self._check_events()
            self.update_sip_position()
            self.bullets.update()
            self._update_screen()
            self._update_aliens()
            # tick the clock at a specific interval
            self.clock.tick(self.settings.clock_frame)

    def _check_events(self):
        """
        Check for events.
        """
        # watch for keyboard and mouse event
        for event in pygame.event.get():
            if (event.type == pygame.QUIT or 
                (event.type == pygame.KEYDOWN and event.key == pygame.K_q)):
                sys.exit()
            # check for spacebar to fire bullets
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self._fire_bullet()
            self.control_ship(event)


    def _fire_bullet(self):
        """
        Create a new bullet and add it to he bullets group.
        """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _draw_bullets(self):
        """
        Update bullet possition and remove old bullets.
        """
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # cleanup old bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
    
    def _update_screen(self):
        """
        Draw display screen.
        """
        # redraw the screen during each pass through the loop, pygame colors uses RGB
        self.screen.fill(self.settings.bg_color)
        # draw and remvoe old bullets
        self._draw_bullets()
        # display aliens
        self.aliens.draw(self.screen)
        # display ship
        self.ship.blitme()
        # Make the most recently draw screen visible (re-draw the screen).
        pygame.display.flip()

    def _create_alien(self, x_position, y_position):
        """
        Create an alien and place it in the row.
        """
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _create_fleet(self):
        """
        Create the fleet o aliens.
        """
        # create an alien and keep adding aliens until there's no room left.
        # Spacing between alins is on aline with
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_x = alien_width
            current_y += 2 * alien_height

    def _update_aliens(self):
        """
        Check if the fleet is at an edge, then update positions.
        """
        self._check_fleet_edges()
        self.aliens.update()

    def _check_fleet_edges(self):
        """
        Respond apropriate if any alines have reached an edge.
        """
        for alien in self.aliens.sprites():
            edge = alien.check_edges()
            if edge:
                self._change_fleet_direction(edge)
                break
    
    def _change_fleet_direction(self, direction):
        """
        Drop the entire fleet and change the fleet's direction.
        """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.alien_direction['direction'] = direction



if __name__ == "__main__":
    # Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()