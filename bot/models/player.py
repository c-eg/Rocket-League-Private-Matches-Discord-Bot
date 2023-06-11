# -*- coding: utf-8 -*-

from discord import Member


class Player:
    def __init__(self, discord_user: Member, mmr: int):
        self.user = discord_user
        self.mmr = mmr

    def get_discord_user(self) -> Member:
        return self.user

    def get_mmr(self) -> int:
        return self.mmr

    def __str__(self) -> str:
        return f"{self.user}: {self.mmr}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Player):
            return NotImplemented

        return self.user == other.user
