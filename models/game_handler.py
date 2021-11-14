# -*- coding: utf-8 -*-

class GameHandler(object):
    def __init__(self, game_size: int, users: list):
        self.game_size = game_size
        self.users = users

    def get_game_size(self):
        return self.game_size

    def get_users(self):
        return self.users
