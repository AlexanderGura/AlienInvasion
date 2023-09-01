class Settings():
    '''Класс для хранения всех настроек игры Alien Invasion.'''

    def __init__(self):
        '''Инициализирует настройки игры.'''
        # Параметры экрана
        self.bg_color = (100, 200, 20)

        # Параметры корабля
        self.ship_speed = 1.5


        # Параметры снаряда
        self.bullet_allowed = 3
        self.bullet_speed = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)