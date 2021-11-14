# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

# TODO: make this abstract class to then create a 'Captains',
# 'Balanced' or 'Random' subclass games


class Game(ABC):
    def __init__(self, players: list):
        self.team_one = []
        self.team_two = []
        self.users = players
        self.users.sort(key=lambda x: x.mmr, reverse=False)

    @abstractmethod
    def assign_teams(self):
        pass

    def get_team_one(self):
        return self.team_one

    def get_team_two(self):
        return self.team_two
