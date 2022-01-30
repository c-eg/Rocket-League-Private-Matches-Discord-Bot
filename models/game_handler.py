# -*- coding: utf-8 -*-


class GameHandler(object):
    def __init__(self, game_size: int, players: list):
        self.game_size = game_size
        self.players = players

    def get_game_size(self):
        return self.game_size

    def get_players(self):
        return self.players
