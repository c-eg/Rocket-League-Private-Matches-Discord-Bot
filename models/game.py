# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class Game(ABC):
    def __init__(self, players: list):
        self.team_one = []
        self.team_two = []
        self.players = players
        self.players.sort(key=lambda x: x.mmr, reverse=False)

    @abstractmethod
    async def assign_teams(self):
        pass

    def get_team_one(self):
        return self.team_one

    def get_team_two(self):
        return self.team_two
