import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingPermissions, MissingRole

import json
from pprint import PrettyPrinter as p
import re
import logging

# Logging
logging.basicConfig(level=logging.INFO)


# Initialize bot and set command prefix as "h."
bot = commands.Bot(command_prefix='h.')
# Bot token
BOT_TOKEN = "NzQ4NjA1MzY1NDc3ODM0Nzcy.X0f3Ew.AhLwFt40bfPJu7VLQ3pcaQu2qwc"


@bot.event
async def on_ready():
    """Prints 'Bot is live!' to the console when the bot is ready"""
    await bot.change_presence(status=discord.Status.idle,
                              activity=discord.Activity(type=discord.ActivityType.playing, name='use prefix "$"'))
    print(f"Bot is live!")


@bot.event
async def on_member_join(member):
    """New member?!"""
    channel = bot.get_channel(748332512371146823)
    await channel.send(f"Welcome to the server {member.mention}!")


@bot.event
async def on_member_remove(member):
    """Did a member just leave?"""
    channel = bot.get_channel(748569304995201045)
    await channel.send(f"{member.mention} has left this server!")


@bot.event
async def on_command_error(ctx, error):
    # """When someone tries to access a unknown command"""
    if isinstance(error, CommandNotFound):
        await ctx.send("Command Not Found!")
        return
    elif isinstance(error, MissingPermissions):
        await ctx.send("You can't use that command. Reason: Missing Perms")
        return
    elif isinstance(error, MissingRole):
        await ctx.send("You can't use that command. Reason: Missing Role")


@bot.command()
async def ping(ctx):
    """What's the latency of the bot?"""
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")


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
        if msg.author == member: count += 1

    await ctx.send(f"{member.display_name} has sent {count} message(s)!")


@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, num: int=5):
    """Wanna delete messages in bunches?"""
    num = 100 if num > 100 else num  # sets num to 100 if num is greater than 100
    await ctx.channel.purge(limit=num)


@bot.command()
@commands.has_role('admin')
async def kick(ctx, member: discord.Member, reason: str = None):
    """Kick function"""
    await member.kick(reason=reason)
    await ctx.send(f"{member.display_name} has been kicked.")


@bot.command()
@commands.has_role('admin')
async def ban(ctx, member: discord.Member, reason: str = None):
    """Ban function"""
    await member.ban(reason=reason)
    await ctx.send(f"{member.display_name} has been banned.")


@bot.command()
@commands.has_role('admin')
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

    all_commands.append('unban (staff only): unbans a member')



# TODO: Make warn command
@bot.command()
@commands.has_role('admin')
async def warn(ctx, member: discord.Member, reason: str = None):
    pass


# TODO: DM the user the names of all the commands
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
    except Exception:
        await ctx.send(f"Commands: \n{cmd}")

bot.run(BOT_TOKEN)
