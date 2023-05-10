import requests
from discord import Embed
from discord.ext import commands

from math import ceil
from random import randint

async def setup(bot):
    await bot.add_cog(Fun(bot))

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def xkcd(self, ctx):
        msg = ctx.message
        req_xkcd = requests.get(url="https://xkcd.com/info.0.json")
        xkcd = req_xkcd.json()

        xkcd_title = f"Comic no. {str(xkcd['num'])}: {xkcd['safe_title']}"
        xkcd_alt = xkcd["alt"]
        xkcd_img = xkcd["img"]
        xkcd_date = f"Published on: {xkcd['day']}/{xkcd['month']}/{xkcd['year']}"
        
        xkcd_embed = Embed(
                            title=xkcd_title,
                            description=xkcd_alt,
                            colour=0x111212
                          )
        xkcd_embed.set_author(
                              name="xkcd",
                              icon_url="https://i.imgur.com/7bD2qfq.png"
                             )
        xkcd_embed.set_image(url=xkcd_img)
        xkcd_embed.set_footer(text=xkcd_date)

        await msg.delete()
        await ctx.message.channel.send(embed=xkcd_embed)

