import sys
import pygame

from time import sleep
from game_stats import GameStats
from settings import Settings
from ship import Ship
from bullet import Bullet
from aliens import Alien
from button import Button

class AlienInvasion:

    def __init__(self):

        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')

        self.clock = pygame.time.Clock()
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.play_button = Button(self, 'Play') 
        
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.last_shot_time = 0

        self._create_fleet()

        self.game_active = False

    def run_game(self):
        
        while True:
            self._check_events()
            self._chech_keys()
            self.ship.update()
            self.bullets.update()
            self._update_aliens()

            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):

        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.stats.reset_stats()

        if self.play_button.rect.collidepoint(mouse_pos):
            self.stats.reset_stats()
            self.game_active = True

            self.bullets.empty()
            self.aliens.empty()

            self._create_fleet()
            self.ship.center_ship()

    def _chech_keys(self):
        
        keys = pygame.key.get_pressed()

        self.ship.moving_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        self.ship.moving_left = keys[pygame.K_LEFT] or keys[pygame.K_a]

        if keys[pygame.K_SPACE]:
            self._fire_bullet()

    def _fire_bullet(self):

        current_time = pygame.time.get_ticks()

        if current_time - self.last_shot_time < self.settings.bullet_cooldown:
            return
        
        if len(self.bullets) >= 5:
            return
        
        new_bullet = Bullet(self.ship)
        self.bullets.add(new_bullet)
        self.last_shot_time = current_time

    def _update_screen(self):

        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self.aliens.draw(self.screen)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _create_fleet(self):

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height

        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):

        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):

        self.aliens.update()

        self._check_fleet_edge()
        self._check_bullet_alien_collision()
        self._check_fleet_destroyed()
        self._check_ship_alien()
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break       

    def _ship_hit(self):

        if self.stats.ship_left > 0:
            self.stats.ship_left -= 1

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.1)
        else:
            self.game_active = False

    def _check_fleet_destroyed(self):

        if not self.aliens:

            self.bullets.empty()
            self._create_fleet()

    def _check_ship_alien(self):

        if pygame.sprite.spritecollideany(
            self.ship, self.aliens
        ):
            print('Game Ower')
            self._ship_hit()

    def _check_bullet_alien_collision(self):
        
        pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

    def _check_fleet_edge(self):
    
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()

"""     #for full screen mod have to use the next in __init__:

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        
"""