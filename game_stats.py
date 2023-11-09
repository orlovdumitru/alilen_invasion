from store_data import StoreData


class GameStats:
    """
    Track statiscs for Alien Invasion.
    """

    def __init__(self, ai_game):
        """
        Initialize statistics.
        """
        self.storage_data = StoreData(ai_game)
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score = self.storage_data.read_top_score()

    def reset_stats(self):
        """
        Initialize statistics that can change during the game.
        """
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
