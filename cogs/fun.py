import discord
import requests
import numpy as np
from discord import Embed
from discord.ext import commands
from math import ceil
from random import randint


class Giveaway(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['memes', 'mem', 'mems'])
    @commands.cooldown(rate=1, per=2, type=commands.BucketType.member)
    async def meme(self, ctx):
        req = requests.get(
            "https://memes.blademaker.tv/api?lang=en")  # some-random-api's isn't fast enought to handle cooldowns
        meme = req.json()
        caption = meme['title']
        image = meme['image']
        author = meme['author']
        msg_embed = Embed(
            description=caption,
            colour=0xeb9bd9
        )
        msg_embed.set_author(
            name=ctx.author.name,
            icon_url=ctx.author.avatar_url
        )
        msg_embed.set_image(
            url=image
        )
        msg_embed.set_footer(text=f"Author • {author}")
        await ctx.send(embed=msg_embed)

    @meme.error
    async def meme_has_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown_period = error.retry_after
            cooldown_period = round(cooldown_period)
            msg_embed = Embed(
                title="Kid, don't get spicy with the memes",
                description=f"You're able to use this command again in {cooldown_period} seconds"
            )
            msg_embed.set_thumbnail(
                url="https://i.imgur.com/j9fUg7T.jpg")  # didn't find any images online, so had to upload my own on imgur
            msg_embed.set_footer(text="Go do some fishing till then")
            await ctx.message.channel.send(embed=msg_embed)

    @commands.command(aliases=['facts', 'fax'])
    async def fact(self, ctx, *, animal=None):
        if animal is None:
            msg_embed_help = Embed(
                title="Command Help",
                description="Here's a list of all the animal you can pick:"
            )
            msg_embed_help.add_field(name="🐶 Dogs", value="`poyo!fact dog`")
            msg_embed_help.add_field(name="🐱 Cats", value="`poyo!fact cat`")
            """
            msg_embed_help.add_field(name="🐳 Whales & Sharks", value="`poyo!fact whsh`")
            msg_embed_help.add_field(name="🐬 Dolphin", value="`poyo!fact dolphin`", inline=True)
            msg_embed_help.add_field(name="🦥 Sloth", value="`poyo!fact sloth`", inline=True)
            msg_embed_help.add_field(name="🐑 Sheep", value="`poyo!fact sheep`", inline=True)
            """
            msg_embed_help.set_footer(text="More comming soon!")
            await ctx.send(embed=msg_embed_help)
        else:
            if animal == "dog":
                req_fact = requests.get(url="https://some-random-api.ml/facts/dog")
                fact = req_fact.json()
                fact = fact["fact"]
                req_img = requests.get(url="https://dog.ceo/api/breeds/image/random")
                img = req_img.json()
                img = img["message"]
                msg_embed = Embed(
                    title="DId YoU KnOW?",
                    description=fact,
                    colour=0xeb9bd9
                )
                msg_embed.set_thumbnail(url=img)
                await ctx.message.channel.send(embed=msg_embed)
            elif animal == "cat":
                req_fact = requests.get(url="https://some-random-api.ml/facts/cat")
                fact = req_fact.json()
                fact = fact["fact"]
                req_img = requests.get(url="https://api.thecatapi.com/v1/images/search")
                img = req_img.json()
                img = img[0]["url"]
                msg_embed = Embed(
                    title="DId YoU KnOW?",
                    description=fact,
                    colour=0xeb9bd9
                )
                msg_embed.set_thumbnail(url=img)
                await ctx.message.channel.send(embed=msg_embed)

    @commands.command()
    async def xkcd(self, ctx):
        msg = ctx.message
        req_xkcd = requests.get(url="https://xkcd.com/info.0.json")
        xkcd = req_xkcd.json()
        xkcd_title = "Comic no. " + str(xkcd["num"]) + ": " + xkcd["safe_title"]
        xkcd_alt = xkcd["alt"]
        xkcd_img = xkcd["img"]
        xkcd_date = "Published on • " + xkcd["day"] + '/' + (
            "0" + xkcd["month"] if len(xkcd["month"]) < 2 else xkcd["month"]) + '/' + xkcd["year"]
        xkcd_embed = Embed(
            title=xkcd_title,
            description=xkcd_alt,
            colour=0x111212
        )
        xkcd_embed.set_author(
            name="xkcd",
            icon_url="https://i.imgur.com/7bD2qfq.png"
        )
        xkcd_embed.set_image(
            url=xkcd_img
        )
        xkcd_embed.set_footer(
            text=xkcd_date
        )
        await msg.delete()
        await ctx.message.channel.send(embed=xkcd_embed)

    @commands.command(aliases=['minesweep', 'ms', 'mine'])
    async def minesweeper(self, ctx):
        # edge cases
        top = [0, 1, 2, 3, 4]
        bottom = [20, 21, 22, 23, 24]
        left = [0, 5, 10, 15, 20]
        right = [4, 9, 14, 19, 24]

        # corner cases
        top_c = [1, 2, 3]
        bottom_c = [21, 22, 23]
        left_c = [5, 10, 15]
        right_c = [9, 14, 19]
        tl = [0]
        bl = [20]
        tr = [4]
        br = [24]

        # v= [5, 9, 12, 19]
        # has all the positions of mines used later to give hints
        # v= [3,4,9,10,11,15,21,23]
        v = []
        # board without mines
        board = [0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0]
        # random gen of mines
        for m in range(ceil(len(board) / 3)):
            # appeneded to the list with indexes of mines
            v.append(randint(0, 24))

        # goes through the list of mines and replaces index of boards
        # with 9 representing mines
        for o in v:
            board[o] = 9
        print(f"Without Hints: {board}\n")

        # adds hints
        for p in v:
            # Adjacent
            #     ^
            # <       >
            #     v
            if p not in bottom and board[p + 5] < 9:
                board[p + 5] += 1
            if p not in top and board[p - 5] < 9:
                board[p - 5] += 1
            if p not in right and board[p + 1] < 9:
                board[p + 1] += 1
            if p not in left and board[p - 1] < 9:
                board[p - 1] += 1
            # Corner
            # o       o
            #
            # o       o
            if p in tl + tr + bl + br:
                if p in tl and board[p + 6] < 9:
                    board[p + 6] += 1
                elif p in bl and board[p - 4] < 9:
                    board[p - 4] += 1
                elif p in tr and board[p + 4] < 9:
                    board[p + 4] += 1
                elif p in br and board[p - 6] < 9:
                    board[p - 6] += 1
            elif p in top_c + bottom_c + left_c + right_c:
                if p in top_c:
                    if board[p + 6] < 9:
                        board[p + 6] += 1
                    if board[p + 4] < 9:
                        board[p + 4] += 1
                if p in bottom_c:
                    if board[p - 6] < 9:
                        board[p - 6] += 1
                    if board[p - 4] < 9:
                        board[p - 4] += 1
                if p in left_c:
                    if board[p + 6] < 9:
                        board[p + 6] += 1
                    if board[p - 4] < 9:
                        board[p - 4] += 1
                if p in right_c:
                    if board[p - 6] < 9:
                        board[p - 6] += 1
                    if board[p + 4] < 9:
                        board[p + 4] += 1
            else:
                if board[p - 6] < 9:
                    board[p - 6] += 1
                if board[p + 4] < 9:
                    board[p + 4] += 1
                if board[p - 4] < 9:
                    board[p - 4] += 1
                if board[p + 6] < 9:
                    board[p + 6] += 1

        print(f"With hints:\n{board[:5]}\n{board[5:10]}\n{board[10:15]}\n{board[15:20]}\n{board[20:]}")

        m = 0

        for e in board:
            if e < 1:
                board[m] = "||:black_large_square:||"
            elif e == 1:
                board[m] = "||:one:||"
            elif e == 2:
                board[m] = "||:two:||"
            elif e == 3:
                board[m] = "||:three:||"
            elif e == 4:
                board[m] = "||:four:||"
            elif e == 5:
                board[m] = "||:five:||"
            elif e == 6:
                board[m] = "||:six:||"
            elif e == 7:
                board[m] = "||:seven:||"
            elif e == 8:
                board[m] = "||:eight:||"
            elif e == 9:
                board[m] = "||:bomb:||"
            m += 1

        first = ''.join(board[:5])
        second = ''.join(board[5:10])
        third = ''.join(board[10:15])
        fourth = ''.join(board[15:20])
        fifth = ''.join(board[20:])

        mc_embed = discord.Embed(
            title=":regional_indicator_m::regional_indicator_i::regional_indicator_n::regional_indicator_e::regional_indicator_s::regional_indicator_w::regional_indicator_e::regional_indicator_e::regional_indicator_p::regional_indicator_e::regional_indicator_r:",
            description=f"{first}\n{second}\n{third}\n{fourth}\n{fifth}"
        )
        await ctx.message.channel.send(embed=mc_embed)

    @commands.command()
    @commands.guild_only()
    async def rush(self, ctx, hp=3):
        e = Embed(title="Command under construction",
                  description="This command is still under construction.").set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Giveaway(bot))
