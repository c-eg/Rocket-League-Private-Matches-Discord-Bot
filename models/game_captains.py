# -*- coding: utf-8 -*-

from models.game import Game


class CaptainsGame(Game):
    def __init__(self, players):
        super(CaptainsGame, self).__init__(self, players)

    def assign_teams(self):
        return
        # TODO: balance teams on user mmr
