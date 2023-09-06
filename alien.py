import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''Класс, представляющий одного прешельца.'''

    def __init__(self, ai_game):
        '''Инициализирует пришельца и задает его начальную позицию.'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Загрузка изображения пришельца и назначения атрибута rect.
        self.load_alien_image()

        # Каждый новый пришелец появляется в левом верхнем углу экрана.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # Сохранение точной горизонтальной позиции пришельца.
        self.x = float(self.rect.x)

    def update(self):
        '''Перемещает пришельца вправо.'''
        self.x += (self.settings.alien_speed_factor 
            * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        '''Возвращает True, если пришелец находится у края экрана.'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def load_alien_image(self):
        if self.stats.level < 5:
            self.image = pygame.image.load('images/alien_green.png')
            self.rect = self.image.get_rect()
        elif self.stats.level < 10:
            self.image = pygame.image.load('images/alien_yellow.png')
            self.rect = self.image.get_rect()
        elif self.stats.level < 20:
            self.image = pygame.image.load('images/alien_red.png')
            self.rect = self.image.get_rect()

class AlienBoss(Alien):
    '''Класс, представляющий финального босса игры.'''

    def __init__(self, ai_game):
        '''Инициализирует атрибуты босса.'''
        super().__init__(ai_game)

        self.image = pygame.image.load('images/boss.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = self.settings.screen_width // 2
        self.rect.y = 100

    def draw(self):
        self.screen.blit(self.image, self.rect)