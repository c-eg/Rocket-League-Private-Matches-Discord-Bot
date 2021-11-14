# -*- coding: utf-8 -*-

from models.game import Game


class BalancedGame(Game):
    def __init__(self, players):
        super(BalancedGame, self).__init__(self, players)

    def assign_teams(self):
        return
        # TODO: balance teams on user mmr
