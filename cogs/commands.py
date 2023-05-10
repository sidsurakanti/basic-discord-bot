from discord.ext import commands
import discord

from datetime import datetime

async def setup(bot):
    await bot.add_cog(Commands(bot=bot))

class Commands(commands.Cog, name="Commands"):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if ctx.guild is None:
            return False
        return True

    @commands.command()
    async def ping(self, ctx):
        """What's the latency of the bot?"""
        pong = discord.Embed(description=f"Pong! {round(self.bot.latency * 1000)}ms")
        pong.set_footer(text=f"Requested by {ctx.author}")
        return await ctx.send(embed=pong)

    @commands.command(aliases=['server_members'])
    async def members(self, ctx):
        """How many members are in the server?"""
        counter = 0 
        for member in self.bot.get_all_members():
            if member.guild == ctx.author.guild and not member.bot:
                counter += 1

        embed = discord.Embed(
                              description=f"Number of users in the server: {counter}",
                              timestamp=ctx.message.created_at
                             )
        await ctx.send(embed=embed)

    @commands.command(aliases=['my_messages'])
    async def messages(self, ctx, member: discord.Member = None):
        """How many messages did I send in this server so far?"""
        member = member or ctx.author
        channel = ctx.channel
        count = 0
        async for msg in channel.history(limit=None):
            if msg.author == member:
                count += 1

        embed = discord.Embed(
                              description=f"{member} has sent {count} messages",
                              timestamp=ctx.message.created_at
                             )
        await ctx.send(embed=embed)

    @commands.command(aliases=['clear'])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, num: int = 5):
        """Deletes messages in bunches"""
        num = max(num, 50)
        await ctx.channel.purge(limit=num)

    @commands.command()
    async def rules(self, ctx):
        """Some basic rules"""
        rules = discord.Embed(title="Server Rules", colour=discord.Colour.magenta())

        rules.add_field(name="Rule 1", value="No racism and polictics", inline=False)
        rules.add_field(name="Rule 2", value="No spamming", inline=False)
        rules.add_field(name="Rule 3", value="Don't send harmful/malicious content", inline=False)
        rules.add_field(name="Rule 4", value="NSFW isn't allowed", inline=False)
        rules.add_field(name="Rule 5", value=r"Follow discord tos (https://www.discord.com/terms)")
        rules.set_footer(text=f"Requested by: {ctx.author}")

        await ctx.send(embed=rules)

    @commands.command(aliases=["userinfo", "whois"])
    async def info(self, ctx, member: discord.Member = None):
        """Basic info about a user"""
        member = member or ctx.author
        # roles user has
        roles = [role.mention for role in member.roles if role.name != "@everyone"]
        # date account was created on
        create_date = member.created_at.strftime("%B %#d, %Y")
        # date user joined server
        join_date = member.joined_at.strftime("%B %#d, %Y")

        # create embed
        userinfo = discord.Embed(
                                colour=discord.Colour.dark_magenta(),
                                timestamp=ctx.message.created_at
                                )
        userinfo.add_field(name="Registered", value=create_date)
        userinfo.add_field(name="Joined", value=join_date)
        userinfo.add_field(
                            name="Roles",
                            value=" ".join(roles), inline=False)
        userinfo.set_author(
                            name=f"{member}", 
                            icon_url=member.display_avatar.url
                            )

        await ctx.send(embed=userinfo)

    @commands.command(aliases=["av", "pfp"])
    async def avatar(self, ctx, member: commands.MemberConverter = None):
        """What's your profile pic?"""
        member = member or ctx.author

        embed = discord.Embed()
        embed.set_author(name=f"{ctx.author}", icon_url=member.display_avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        embed.set_image(url=member.display_avatar.url)

        await ctx.send(embed=embed)

    @commands.command(aliases=["new_poll"])
    async def poll(self, ctx, desc):
        """Make a poll!"""
        await ctx.message.delete()

        msg = discord.Embed(title=f"Poll", description=desc, colour=discord.Colour.dark_teal())
        msg.set_footer(text=f"Requested by {ctx.author.display_name}")
        msg = await ctx.send(embed=msg)

        await msg.add_reaction('👍')
        await msg.add_reaction('👎')


