class GameStats():
    '''Отслеживание статистики для игры Alien Invasion.'''

    def __init__(self, ai_game):
        '''Инициирует статистику.'''
        self.settings = ai_game.settings
        self.reset_stats()

        # Игра запукается в неактивном состоянии.
        self.game_active = False

    def reset_stats(self):
        self.ship_left = self.settings.ship_limit