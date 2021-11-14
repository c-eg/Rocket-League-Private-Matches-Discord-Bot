# -*- coding: utf-8 -*-

from models.game import Game
import random


class RandomGame(Game):
    def __init__(self, players):
        super(RandomGame, self).__init__(players)

    async def assign_teams(self):
        random.shuffle(self.players)
        self.team_one = self.players[:3]
        self.team_two = self.players[-3:]
