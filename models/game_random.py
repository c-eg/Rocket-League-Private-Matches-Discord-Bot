# -*- coding: utf-8 -*-

from models.game import Game
import random


class RandomGame(Game):
    def __init__(self, players):
        super(RandomGame, self).__init__(players)

    def assign_teams(self):
        random.shuffle(self.__users)
        self.__team_one = self.__users[:3]
        self.__team_two = self.__users[-3:]
