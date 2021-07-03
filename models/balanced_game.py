from abc import ABC

from models.game import Game


class BalancedGame(Game, ABC):
    def __init__(self, players):
        super().__init__(players)

    def assign_teams(self):
        return
        # TODO: balance teams on user mmr
