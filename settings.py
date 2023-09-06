class Settings():
    '''Класс для хранения всех настроек игры Alien Invasion.'''

    def __init__(self):
        '''Инициализирует статические настройки игры.'''
        # Параметры экрана
        self.bg_color = (100, 200, 20)

        # Параметры кнопок
        self.button_width = 100
        self.button_height = 50

        # Параметры корабля
        self.ship_limit = 3

        # Параметры пришельцев
        self.alien_drop_speed = 10

        # Параметры снаряда
        self.bullet_allowed = 3
        self.bullet_width = 1000
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)

        # Темп ускорения игры.
        self.speedup_scale = 1.05
        # Темп роста стоймости пришельцев.
        self.score_scale = 1.5

        self.initialize_dinamic_settings()

    def initialize_dinamic_settings(self):
        '''Инициализирует настройки, изменяющиеся в ходе игры.'''
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 1.5
        self.alien_speed_factor = 1.5
        self.fleet_direction = 1    # 1 - движение вправо, -1 влево

        # Подсчёт очков
        self.alien_points = 50
    
    def increase_speed(self):
        '''Увеличивает настройки скорости и стоймость пришельцев.'''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
