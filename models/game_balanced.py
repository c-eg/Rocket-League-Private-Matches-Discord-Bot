# -*- coding: utf-8 -*-

from itertools import permutations

from models.game import Game


class BalancedGame(Game):
    def __init__(self, players):
        super(BalancedGame, self).__init__(players)

    async def assign_teams(self):
        range = 99999999999

        perms = list(permutations(self.players))

        for perm in perms:
            temp_one = perm[:3]
            temp_two = perm[-3:]
            temp_range = abs(sum([player.get_mmr() for player in temp_one]) - sum(player.get_mmr() for player in temp_two))

            if temp_range < range:
                self.team_one = temp_one
                self.team_two = temp_two
                range = temp_range
