# -*- coding: utf-8 -*-

from discord.ext import commands
from asyncio import TimeoutError

from models.game import Game
from models.no_player_action_exception import NoPlayerActionException


class CaptainsGame(Game):
    def __init__(self, players, ctx: commands.Context, bot):
        super(CaptainsGame, self).__init__(players)
        self.ctx = ctx
        self.bot = bot

    async def assign_teams(self):
        captain_a = self.players.pop(0)
        # captain_b = self.players.pop(0)

        print(f"CAP A: {captain_a}")
        # print(f"CAP B: {captain_b}")

        captain_a_message = "Please pick a player to be on your team, type the number corresponding to the player e.g. 2\n\n"

        counter = 1

        for player in self.players:
            captain_a_message += f"{counter}) {player.get_discord_user().mention}\n"
            counter += 1

        disc_message = await captain_a.get_discord_user().send(captain_a_message)

        try:
            reply = await self.bot.wait_for(event='message', timeout=60, check=lambda message: message.channel == disc_message.channel)
        except TimeoutError:
            raise NoPlayerActionException()

        reply = int(reply)

        """
        TODO:
        - Get bot to send a message to user if they don't send a number in the correct range.
        - Then remove that user from the queue, add to team 1
        - Then let captain 2 choose two players
        - Then assign last player to team 1
        """

        if not 1 <= reply <= len(self.players):


        print(reply.content)
