from discord.ext import commands
import discord


def setup(bot):
    bot.add_cog(Commands(bot=bot))


class Commands(commands.Cog, name="Commands"):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if ctx.guild is None:
            return False
        return True

    @commands.command()
    async def ping(self,ctx):
        return await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command()
    async def members(self,ctx):
        """How many members are in the server?"""
        await ctx.send(f"Number of users in the server: {len(self.bot.users)}")

    @commands.command()
    async def messages(self,ctx, member: discord.Member = None):
        """How many messages did I send?"""
        member = ctx.author if member is None else member
        channel = ctx.channel
        count = 0
        async for msg in channel.history(limit=None):
            if msg.author == member:
                count += 1

        await ctx.send(f"{member.display_name} has sent {count} message(s)!")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self,ctx, num: int = 5):
        """Wanna delete messages in bunches?"""
        num = 100 if num > 100 else num  # sets num to 100 if num is greater than 100
        await ctx.channel.purge(limit=num)

    @commands.command()
    async def commands(self,ctx):
        all_commands = ['kick (staff only): kicks a member',
                        'ban (staff only): bans a member',
                        'purge (staff only): bunch delete',
                        'messages: returns the number of messages a member sent',
                        'members: returns the total number of members in the server',
                        'ping: returns the latency of the bot']

        user = self.bot.get_user(ctx.author.id)
        cmd = '\n'.join(all_commands)
        try:
            await user.send(f"Commands: \n{cmd}")
        except:
            await ctx.send(f"Commands: \n{cmd}")


