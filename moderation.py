from discord.ext import commands
import discord


def setup(bot):
    bot.add_cog(Moderation(bot=bot))


class Moderation(commands.Cog, name="Moderation"):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if ctx.guild is None:
            return False
        return True

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason: str = None):
        """Kick function"""
        await member.kick(reason=reason)
        await ctx.send(f"{member.display_name} has been kicked.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason: str = None):
        """Ban function"""
        await member.ban(reason=reason)
        await ctx.send(f"{member.display_name} has been banned.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        """Unban function"""
        banned_users = await ctx.guild.bans()
        member_name, member_id = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user
            if (member_name, member_id) == (user.name, user.discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{user.mention} has been unbanned!")
                return

    # TODO: Make warn command
    @commands.command()
    @commands.has_permissions(manage_roles=True, ban_members=True)
    async def warn(self, ctx, member: discord.Member, reason: str = None):
        pass

