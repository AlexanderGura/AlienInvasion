import pygame.font
from pygame.sprite import Sprite

class Button(Sprite):
    '''Класс для реализации кнопок и их возможностей.'''

    def __init__(self, ai_game, msg, x, y):
        '''Инициализирует атрибуты кнопки.'''
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Назначение размеров и свойств кнопок.
        self.width = self.settings.button_width
        self.height = self.settings.button_height
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 72)

        # Построение объекта rect кнопки и выравнивание по центру экрана.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.x, self.rect.y = x, y

        # Сообщение кнопки создается только один раз.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        '''Преобразует msg в прямоугольник и выравнивает текст по центру.'''
        self.msg_image = self.font.render(msg, True,
                                self.text_color, None)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        '''Отображение пустой кнопки и вывод изображения.'''
        self.screen.blit(self.msg_image, self.msg_image_rect)