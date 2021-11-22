# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from asyncio import TimeoutError
import time

from models.game import Game
from models.no_player_action_exception import NoPlayerActionException
from static import EmbedTemplate


embed_template = EmbedTemplate(
    title="Captains will now pick teams!", colour=discord.Colour.teal()
)


class CaptainsGame(Game):
    def __init__(self, players, ctx: commands.Context, bot):
        super(CaptainsGame, self).__init__(players)
        self.ctx = ctx
        self.bot = bot

    async def assign_teams(self):
        """
        Assigns teams based on the two captains choices.
        """
        captain_a = self.players.pop(0)
        captain_b = self.players.pop(0)

        embed = embed_template.copy()

        embed.add_field(
            name=f"Captain 1!",
            value=f"{captain_a.get_discord_user().mention}",
            inline=False,
        )
        embed.add_field(
            name=f"Captain 2!",
            value=f"{captain_b.get_discord_user().mention}",
            inline=False,
        )

        # CAPTAIN A FIRST PICK
        captain_a_message = "You have 90 seconds to pick.\nPlease pick a player to be on your team, type the number corresponding to the player e.g. 2\n\n"
        counter = 1

        for player in self.players:
            captain_a_message += f"{counter}) {player.get_discord_user().mention}\n"
            counter += 1

        disc_message = await captain_a.get_discord_user().send(captain_a_message)

        listen_for_captain_a = True
        time_start = time.time() + 90

        while not listen_for_captain_a:
            try:
                reply = await self.bot.wait_for(
                    event="message",
                    timeout=time_start - time.time(),
                    check=lambda message: message.channel == disc_message.channel,
                )
                reply = int(reply)

                if 1 <= reply <= 4:
                    listen_for_captain_a = False
                    await captain_a.get_discord_user().send(
                        f"You picked: {self.players[reply - 1].get_discord_user().mention}"
                    )
                    self.team_one.append(self.players.pop(reply - 1))
                else:
                    await captain_a.get_discord_user().send(
                        "Please enter a number between 1 and 4!"
                    )
            except TimeoutError:
                listen_for_captain_a = False
                raise NoPlayerActionException()

        # CAPTAIN B FIRST PICK
        captain_b_message = "You have 2 minutes to pick.\nPlease pick a player to be on your team, type the number corresponding to the player e.g. 2\n\n"
        counter = 1

        for player in self.players:
            captain_a_message += f"{counter}) {player.get_discord_user().mention}\n"
            counter += 1

        disc_message = await captain_b.get_discord_user().send(captain_b_message)

        listen_for_captain_b = True
        time_start = time.time() + 120

        while listen_for_captain_b:
            try:
                reply = await self.bot.wait_for(
                    event="message",
                    timeout=time_start - time.time(),
                    check=lambda message: message.channel == disc_message.channel,
                )
                reply = int(reply)

                if 1 <= reply <= 3:
                    listen_for_captain_a = False
                    await captain_a.get_discord_user().send(
                        f"You picked: {self.players[reply - 1].get_discord_user().mention}"
                    )
                    self.team_two.append(self.players.pop(reply - 1))
                else:
                    await captain_a.get_discord_user().send(
                        "Please enter a number between 1 and 3!"
                    )
            except TimeoutError:
                listen_for_captain_a = False
                raise NoPlayerActionException()

        # CAPTAIN B SECOND PICK
        captain_b_message = "Please pick another player to be on your team, type the number corresponding to the player e.g. 2\n\n"
        counter = 1

        for player in self.players:
            captain_a_message += f"{counter}) {player.get_discord_user().mention}\n"
            counter += 1

        disc_message = await captain_b.get_discord_user().send(captain_b_message)

        listen_for_captain_b = True

        while listen_for_captain_b:
            try:
                reply = await self.bot.wait_for(
                    event="message",
                    timeout=time_start - time.time(),
                    check=lambda message: message.channel == disc_message.channel,
                )
                reply = int(reply)

                if 1 <= reply <= 2:
                    listen_for_captain_a = False
                    await captain_a.get_discord_user().send(
                        f"You picked: {self.players[reply - 1].get_discord_user().mention}"
                    )
                    self.team_two.append(self.players.pop(reply - 1))
                else:
                    await captain_a.get_discord_user().send(
                        "Please enter the number 1 or 2!"
                    )
            except TimeoutError:
                listen_for_captain_a = False
                raise NoPlayerActionException()

        # ASSIGN CAPTAIN A (Team 1) LAST PLAYER
        self.team_one.append(self.players.pop(0))

        # ASSIGN CAPTAIN A TO TEAM 1 AND CAPTAIN B TO TEAM 2
        self.team_one.insert(0, captain_a)
        self.team_two.insert(0, captain_b)
