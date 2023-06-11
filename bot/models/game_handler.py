# -*- coding: utf-8 -*-

from typing import List

from models.player import Player


class GameHandler:
    def __init__(self, game_size: int, players: List[Player]):
        self.game_size = game_size
        self.players = players

    def get_game_size(self) -> int:
        return self.game_size

    def get_players(self) -> List[Player]:
        return self.players
