# -*- coding: utf-8 -*-
import discord


class EmbedTemplate:
    def __init__(self, title, colour):
        self.emb_temp = discord.Embed(
            title=title,
            colour=colour,
        )
        self.emb_temp.set_footer(
            text="UEA Private Matches by curpha",
            icon_url="https://cdn.akamai.steamstatic.com/steamcommunity/public/images/avatars/be/bed810f8bebd7be235b8f7176e3870de1006a6e5_full.jpg",
        )
