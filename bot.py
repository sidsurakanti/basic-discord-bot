import asyncio

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingPermissions, MissingRole, MissingRequiredArgument

import json
import re
import logging
from config import *

# Logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and set command prefix as "h."
# bot = commands.Bot(command_prefix='h.')
# Bot token
# BOT_TOKEN = "NzQ4NjA1MzY1NDc3ODM0Nzcy.X0f3Ew.AhLwFt40bfPJu7VLQ3pcaQu2qwc"


class Heather(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=kwargs.pop('command_prefix', 'h.'),
                         case_insensitive=True,
                         **kwargs)

    async def on_ready(self):
        """Prints 'Bot is live!' to the console when the bot is ready"""
        await self.change_presence(status=discord.Status.idle,
                                   activity=discord.Activity(type=discord.ActivityType.playing, name='use prefix "$"'))

        print(f"Bot is live!")

    async def process_commands(self, message):
        if message.author.bot:
            return

        ctx = await self.get_context(message=message)

        await self.invoke(ctx)

    async def on_member_join(self, member):
        """New member?!"""
        channel = self.get_channel(748332512371146823)
        await channel.send(f"Welcome to the server {member.mention}!")

    async def on_member_remove(self, member):
        """Did a member just leave?"""
        channel = self.get_channel(748569304995201045)
        await channel.send(f"{member.mention} has left this server!")

    async def on_command_error(self, ctx, error):
        """When someone tries to access a unknown command"""
        if isinstance(error, CommandNotFound):
            return await ctx.send("Command Not Found!")
        elif isinstance(error, MissingPermissions):
            return await ctx.send("You can't use that command. Reason: Missing Perms")
        elif isinstance(error, MissingRole):
            return await ctx.send("You can't use that command. Reason: Missing Role")
        elif isinstance(error, MissingRequiredArgument):
            return await ctx.send("Missing Required Parameter")
        else:
            raise error

    async def setup(self, **kwargs):
        try:
            await self.start(BOT_TOKEN, **kwargs)
        except KeyboardInterrupt:
            await self.close()


bot = Heather()


@bot.command()
async def ping(ctx):
    return await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")


@bot.command()
async def members(ctx):
    """How many members are in the server?"""
    await ctx.send(f"Number of users in the server: {len(bot.users)}")


@bot.command()
async def messages(ctx, member: discord.Member = None):
    """How many messages did I send?"""
    member = ctx.author if member is None else member
    channel = ctx.channel
    count = 0
    async for msg in channel.history(limit=None):
        if msg.author == member:
            count += 1

    await ctx.send(f"{member.display_name} has sent {count} message(s)!")


@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, num: int = 5):
    """Wanna delete messages in bunches?"""
    num = 100 if num > 100 else num  # sets num to 100 if num is greater than 100
    await ctx.channel.purge(limit=num)


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, reason: str = None):
    """Kick function"""
    await member.kick(reason=reason)
    await ctx.send(f"{member.display_name} has been kicked.")


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, reason: str = None):
    """Ban function"""
    await member.ban(reason=reason)
    await ctx.send(f"{member.display_name} has been banned.")


@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    """Unban function"""
    banned_users = await ctx.guild.bans()
    member_name, member_id = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user
        if (member_name, member_id) == (user.name, user.discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} has been unbanned!")
            return

    # all_commands.append('unban (staff only): unbans a member')


# TODO: Make warn command
@bot.command()
@commands.has_permissions(administrator=True)
async def warn(ctx, member: discord.Member, reason: str = None):
    pass


@bot.command()
async def commands(ctx):
    all_commands = ['kick (staff only): kicks a member',
                    'ban (staff only): bans a member',
                    'purge (staff only): bunch delete',
                    'messages: returns the number of messages a member sent',
                    'members: returns the total number of members in the server',
                    'ping: returns the latency of the bot']

    user = bot.get_user(ctx.author.id)
    cmd = '\n'.join(all_commands)
    try:
        await user.send(f"Commands: \n{cmd}")
    except:
        await ctx.send(f"Commands: \n{cmd}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.setup())
