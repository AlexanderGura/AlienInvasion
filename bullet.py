import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''Класс для управления снарядами, выпущенными кораблём.'''

    def __init__(self, ai_game):
        '''Создает объект снаряда в текущей позиции корабля.'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Создание снаряда в позиции (0, 0) и назначение правильной позиции.
        self.image = pygame.image.load("images/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.midtop = ai_game.ship.rect.midtop
        self.rect.height = self.settings.bullet_height
        self.rect.width = self.settings.bullet_width

        # Позиция снаряда хранится в вещественном формате.
        self.y = float(self.rect.y)

    def update(self):
        '''Перемещение снаряда вверх по экрану.'''
        # Обновление позиции снаряда в вещественном формате.
        self.y -= self.settings.bullet_speed_factor

        # Обновление позиции прямоугольника.
        self.rect.y = self.y

    def draw_bullet(self):
        '''Вывод снаряда на экран.'''
        self.screen.fill((0, 0, 0), self.rect)