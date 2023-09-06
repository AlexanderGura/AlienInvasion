import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    '''Класс для управления кораблем.'''

    def __init__(self, ai_screen, settings):
        '''Инициирует корабль и задает его начальную позицию.'''
        super().__init__()
        self.screen = ai_screen
        self.screen_rect = ai_screen.get_rect()
        self.settings = settings

        # Загружает изображение корабля и получает прямоугольник.
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()

        # Каждый новый корабль появляется у нижнего края экрана.
        self.rect.midbottom = self.screen_rect.midbottom

        # Сохранение вещественной координаты центра корабля.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Флаги перемещения
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        '''Обновляет позицию корабля с учетом флага.'''
        # Изменяем атрибут x, а не rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed_factor

        if self.moving_up and self.rect.top > 0 :
            self.y -= self.settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed_factor

        # Обновление атрибута rect на основании self.x
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        '''Рисует корабль в текущей позиции.'''
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        '''Размещает корабль в центре нижней стороны.'''
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)