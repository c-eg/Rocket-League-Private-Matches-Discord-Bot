# -*- coding: utf-8 -*-

from models.game import Game


class GameHandler(object):
    def __init__(self, game_size, users):
        self.__game_size = game_size
        self.__users = users[:]  # deep copy

    def get_game_size(self):
        return self.__game_size

    def get_users(self):
        return self.__users
