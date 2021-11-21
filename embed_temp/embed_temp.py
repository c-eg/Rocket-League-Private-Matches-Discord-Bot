# -*- coding: utf-8 -*-

class Embed_Template:
    def __init__(self, embed_title):
        self.emb_temp = discord.Embed(
            title=embed_title, colour=discord.Colour.teal()
        )
        self.emb_temp.set_footer(
            text="UEA Private Matches by curpha",
            icon_url="https://cdn.akamai.steamstatic.com/steamcommunity/public/images/avatars/be/bed810f8bebd7be235b8f7176e3870de1006a6e5_full.jpg",
        )