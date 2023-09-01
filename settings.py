class Settings():
    '''Класс для хранения всех настроек игры Alien Invasion.'''

    def __init__(self):
        '''Инициализирует настройки игры.'''
        # Параметры экрана
        self.bg_color = (100, 200, 20)

        # Параметры корабля
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Параметры пришельцев
        self.alien_speed = 3.0
        self.alien_drop_speed = 30
        self.fleet_direction = 1    # 1 - движение вправо, -1 влево

        # Параметры снаряда
        self.bullet_allowed = 3
        self.bullet_speed = 1.5
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)