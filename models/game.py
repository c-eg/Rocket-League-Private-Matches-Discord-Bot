# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

# TODO: make this abstract class to then create a 'Captains',
# 'Balanced' or 'Random' subclass games


class Game(ABC):
    def __init__(self, players: list):
        self.__team_one = []
        self.__team_two = []
        self.__users = players
        self.__users.sort(key=lambda x: x.__mmr, reverse=False)

    @abstractmethod
    def assign_teams(self):
        pass

    def get_team_one(self):
        return self.__team_one

    def get_team_two(self):
        return self.__team_two
