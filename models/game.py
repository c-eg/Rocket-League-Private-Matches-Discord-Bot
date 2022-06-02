# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import List

from models.player import Player


class Game(ABC):
    def __init__(self, players: List[Player]):
        self.team_one = []
        self.team_two = []
        self.players = players
        self.players.sort(key=lambda x: x.mmr, reverse=True)

    @abstractmethod
    async def assign_teams(self):
        pass

    def get_team_one(self) -> List[Player]:
        return self.team_one

    def get_team_two(self) -> List[Player]:
        return self.team_two
