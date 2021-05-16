import discord

# TODO: make this abstract class to then create a 'Captains',
# 'Balanced' or 'Random' subclass games


class Game(object):
    def __init__(self, users):
        self.__team_one = []
        self.__team_two = []

        self.assign_teams(users)

    async def assign_teams(self, users):
        pass
        # TODO: Assign teams here
