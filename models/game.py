# -*- coding: utf-8 -*-

import abc

# TODO: make this abstract class to then create a 'Captains',
# 'Balanced' or 'Random' subclass games


class Game:
    __metaclass__ = abc.ABCMeta

    def __init__(self, players: list):
        self.__team_one = []
        self.__team_two = []
        players.sort(key=lambda x: x.__mmr, reverse=False)
        self.__users = players

    @abc.abstractmethod
    def assign_teams(self):
        return

    def get_team_one(self):
        return self.__team_one

    def get_team_two(self):
        return self.__team_two
