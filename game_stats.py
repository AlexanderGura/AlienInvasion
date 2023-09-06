class GameStats():
    '''Отслеживание статистики для игры Alien Invasion.'''

    def __init__(self, ai_game):
        '''Инициирует статистику.'''
        self.settings = ai_game.settings
        self.reset_stats()

        # Рекорд не должен сбрасываться.
        self.high_score = 0

        # Игра запукается в неактивном состоянии.
        self.game_active = False
        self.settings_active = False

    def reset_stats(self):
        '''Инициализирует настройки, изменяющиеся в ходе игры.'''
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1