import discord


class Game(object):
    def __init__(self, users):
        self.__team_one = set()
        self.__team_two = set()

        self.assign_teams(users)

    async def assign_teams(self, users):
        pass
        # TODO: Assign teams here
