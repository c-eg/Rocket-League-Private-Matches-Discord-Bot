from abc import ABC

import game

class BalancedGame(game.Game, ABC):
    def __init__(self, players):
        super().__init__(players)

    def assign_teams(self):
        return
        # TODO: balance teams on user mmr
