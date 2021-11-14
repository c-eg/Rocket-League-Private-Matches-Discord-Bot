# -*- coding: utf-8 -*-

from models.game import Game
import random


class RandomGame(Game):
    def __init__(self, players):
        super(RandomGame, self).__init__(players)

    def assign_teams(self):
        random.shuffle(self.users)
        self.team_one = self.users[:3]
        self.team_two = self.users[-3:]
