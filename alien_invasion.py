import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    '''Класс для управления ресурсами и поведением игры.'''

    def __init__(self):
        '''Инициирует игры и создает игровые ресурсы.'''
        pygame.init()               # Иницирует настройки библиотеки Pygame

        self.settings = Settings()  # Отвечает за настройки игры

        # Создает окно в полноэкранном режиме и обновляет настройки
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height


        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self.screen, self.settings)
        self.bullets = pygame.sprite.Group()    # Группировка всех снарядов
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        self.image = pygame.image.load('images/space.jpg')
        self.screen_rect = self.screen.get_rect()

    def run_game(self):
        '''Запуск основного цикла игры.'''
        while True:     # Бесконечный цикл анимации
            self._chech_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()

    def _chech_events(self):
        '''Отслеживание нажатий клавиатуры и мыши.'''
        for event in pygame.event.get():    # Цикл игровых событий
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        '''Реагирует на нажатие клавиш.'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        '''Реагирует на отпускание клавиш.'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        '''Создание нового снаряда и включение его в группу bullets.'''
        # Ограничение на количество выпущенных пуль.
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        '''Создание флота вторжения.'''
        # Создание пришельца и вычисление количества пришельцев в ряду
        # Интервал между соседними пришельцами равен ширине пришельца.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Определяет количество рядов, помещающихся на экране
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                                (3 * alien_height + ship_height))
        number_rows = available_space_y // (2 * alien_height)

        # Создание первого ряда пришельцев.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        '''Создание пришельца и размещение его в ряду.'''
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        '''Реагирует на достижение пришельцем края экрана.'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        '''Опускает весь флот и меняет направление флота.'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.alien_drop_speed
        self.settings.fleet_direction *= -1

    def _update_bullets(self):
        '''Обновляет позиции новых снарядов и удаляет старые.'''
        self.bullets.update()
        # Перебираем группу bullets и удаляем снаряды, вышедшие за границы.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_aliens(self):
        '''Проверяет достиг ли флот края экрана, если нет, то 
            обновляет позиции всех пришельцев в флоте.'''
        self._check_fleet_edges()
        self.aliens.update()

    def _update_screen(self):
        '''Обновляет изображение на экране и отображает новый.'''
        self.screen.blit(self.image, self.screen_rect)
        self.ship.blitme()

        # Перебираем список всех спрайтов(пуль) и рисуем их на экране.
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Отображение последнего прорисованного экрана.
        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()