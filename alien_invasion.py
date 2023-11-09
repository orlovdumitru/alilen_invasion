import sys
from time import sleep
import pygame

from config.settings import Settings
from bullet import Bullet
from ship import Ship
from game_stats import GameStats
from ship_control import ShipControl
from alien import Alien
from button import Button
from scoreboard import Scoreboard
from store_data import StoreData


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
        # create stats instance to store game statistic
        self.stats = GameStats(self)
        self.score_board = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        # start alien invasion in an inactive state.
        self.game_active = False
        # make the play button
        self.play_button = Button(self, "Play")


    def run_game(self):
        """
        Start the main loop for the game.
        """
        while True:
            self._check_events()
            if self.game_active:
                self.update_sip_position()
                self.bullets.update()
                self._update_aliens()
            self._update_screen()
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            self.control_ship(event)


    def _check_every_collision(self, collisions):
        """
        Check every single collision bullets and aliens.
        """
        for aliens in collisions.values():
            self.stats.score += self.settings.alien_points * len(aliens)
        self.score_board.prepare_score()
        self.score_board.check_high_score()

    def _check_bullet_alien_collisions(self):
        """
        Check for any bullets that hit aliens.
        if so, get rid of the bullet and the alien.
        """
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        # regenerate aliens if all are killed
        if collisions:
           self._check_every_collision(collisions)

        if not self.aliens:
            self.bullets.empty() # empty all bullets
            self._create_fleet() # create new aliens
            self.settings.increase_speed()
            # Increase level
            self.stats.level += 1
            self.score_board.prep_level()

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
        self._check_bullet_alien_collisions()
    
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
        self.score_board.show_score()
        self._display_play_button()
        # display ship
        self.ship.blitme()
        # Make the most recently draw screen visible (re-draw the screen).
        pygame.display.flip()

    def _display_play_button(self):
        """
        Draw the play button if the game is inactive.
        """
        if not self.game_active:
            self.play_button.draw_button()

    def _check_play_button(self, position):
        """
        Start new game when the player clicks Play.
        """
        button_clicked = self.play_button.rect.collidepoint(position)
        if button_clicked and not self.game_active:
            # reset the game settings
            self.settings.initialize_dynamic_settings()
            # reset the hame statistics.
            self.stats.reset_stats()
            self.game_active = True
            # get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()
            # create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            # hide the mouse cursor
            pygame.mouse.set_visible(False)
            self.score_board.prep_ships()
            self.score_board.prepare_score()
            self.score_board.prep_level()

    def _check_aliens_bottom(self):
        """
        Check if any aliens have reached the bottom of the screen.
        """
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _ship_hit(self):
        """
        Respond to the ship being hit by an alien.
        """
        if self.stats.ships_left > 0:
            # Decrese number of ships
            self.stats.ships_left -= 1
            # Get rid of any remaining bullets and aliens
            self.score_board.prep_ships()
            self.bullets.empty()
            self.aliens.empty()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            sleep(2)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

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
        # look for alien and ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # look for aliens that hit the bottom of the screen
        self._check_aliens_bottom()

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