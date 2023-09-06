import sys
import pygame

from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien, AlienBoss
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard

class AlienInvasion:
    '''Класс для управления ресурсами и поведением игры.'''

    def __init__(self):
        '''Инициирует игры и создает игровые ресурсы.'''
        pygame.init()               # Иницирует настройки библиотеки Pygame

        self.settings = Settings()  # Отвечает за настройки игры

        # Создает окно в полноэкранном режиме и обновляет настройки
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.settings.screen_width = self.screen_rect.width
        self.settings.screen_height = self.screen_rect.height

        # Создание экземпляров для хранения игровой статистики и результатов.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self.screen, self.settings)
        self.bullets = pygame.sprite.Group()    # Группировка всех снарядов

        # Создание пришельцев, их флота и босса.
        self.aliens = pygame.sprite.Group()
        self.boss = AlienBoss(self)
        self.boss_active = False
        self._create_fleet()

        # Загрузка картинок для игры.
        self.menu_image = pygame.image.load('images/menu.jpg')
        self.game_image = pygame.image.load('images/space.jpg')

        # Создание кнопок для главного меню.
        self.create_buttons()

    def run_game(self):
        '''Запуск основного цикла игры.'''
        while True:     # Бесконечный цикл анимации
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                if self.boss_active:
                    self._update_boss_alien()
                else:
                    self._update_aliens()
                
            self._update_screen()

    def create_buttons(self):
        '''Создает кнопки Play, Settings, Quit.'''
        self.buttons = pygame.sprite.Group()

        x, y = self.screen_rect.center
        diff = self.settings.button_height
        self.play_button = Button(self, "Play", x, y - diff)
        self.settings_button = Button(self, "Settings", x, y)
        self.quit_button = Button(self, "Quit", x, y + diff)

    def _check_events(self):
        '''Отслеживание нажатий клавиатуры и мыши.'''
        for event in pygame.event.get():    # Цикл игровых событий
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_setting_button(mouse_pos)
                self._check_quit_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        '''Запускает новую игру при нажитии кнопки Play.'''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Сброс игровой статистики.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_images()

            # Сброс игровых настроек.
            self.settings.initialize_dinamic_settings()

            # Очистка списков пришельцев и снарядов.
            self.aliens.empty()
            self.bullets.empty()

            # Сознание нового флота и размещение корабля в центре.
            self._create_fleet()
            self.ship.center_ship()

            # Указатель мыши скрывается.
            pygame.mouse.set_visible(False)

    def _check_setting_button(self, mouse_pos):
        '''Проверяет нажатие клавиши Settings.'''
        if self.settings_button.rect.collidepoint(mouse_pos):
            self.stats.settings_active = True

    def _check_quit_button(self, mouse_pos):
        '''Проверяет нажатие клавиши Quit.'''
        if self.quit_button.rect.collidepoint(mouse_pos):
            sys.exit()

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
        elif event.key == pygame.K_ESCAPE:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
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
        if not self.boss_active:
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

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        '''Обработка коллизий снарядов с пришельцами.'''
        # Удаление снарядов и пришельцев, участвующих в коллизиях.
        # collisions - словарь, где ключ - bullet, а значение - aliens
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, False, True)
        
        # Когда кончились пришельцы - создаем новый флот и удаляем снаряды.
        if not self.aliens:
            self.start_new_level()

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

    def start_new_level(self):
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()

        # Увеличение уровня. 
        self.stats.level += 1
        if self.stats.level == 2:
            self.boss_active = True
        self.sb.prep_level() 

    def _check_aliens_bottom(self):
        '''Проверяет, добрались ли пришельцы до нижнего края экрана.'''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_aliens(self):
        '''Проверяет достиг ли флот края экрана, если нет, то 
            обновляет позиции всех пришельцев в флоте.'''
        self._check_fleet_edges()
        self.aliens.update()

        # Проверка коллизий "пришелец - корабль".
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Проверить, добрались ли пришельцы до края экрана.
        self._check_aliens_bottom()

    def _update_boss_alien(self):
        '''Отвечает за обновление позиции босса пришельцев.'''
        if self.boss.check_edges():
            self._change_fleet_direction()
        self.boss.update()

    def _ship_hit(self):
        '''Обрабатывает столкновение корабля с пришельцем.'''
        if self.stats.ship_left > 0:
            # Уменьшение ship_left и обновление панели счёта.
            self.stats.ship_left -= 1
            self.sb.prep_ships()

            # Очистка списков пришельцев и снарядов.
            self.aliens.empty()
            self.bullets.empty()

            # Сознание нового флота и размещение корабля в центре.
            self._create_fleet()
            self.ship.center_ship()

            # Пауза.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        '''Обновляет изображение на экране и отображает новый.'''
        if self.stats.game_active:
            self.screen.blit(self.game_image, self.screen_rect)
            self.ship.blitme()

            # Перебираем список всех спрайтов(пуль) и рисуем их на экране.
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.sb.show_score()
            if self.boss_active:
                self.boss.draw()
            else:
                self.aliens.draw(self.screen)

        # Кнопки отображаются в том случае, если
        # Игра неактива и не вызвано меню настроек.
        if not self.stats.game_active and not self.stats.settings_active:
            self.screen.blit(self.menu_image, self.screen_rect)
            self.play_button.draw_button()
            self.settings_button.draw_button()
            self.quit_button.draw_button()
        # Вызывается, когда включается меню настроек.
        elif self.stats.settings_active:
            self.screen.fill((0, 0, 0), self.screen_rect)

        # Отображение последнего прорисованного экрана.
        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
    sys.pause()