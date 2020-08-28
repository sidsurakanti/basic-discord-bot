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
    async def ping(self, ctx):
        """What's the latency/ping of the bot?"""
        return await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command()
    async def members(self, ctx):
        """How many members are in the server?"""
        member_guild = ctx.author.guild
        counter = 0
        for member in self.bot.get_all_members():
            if member.guild == member_guild and member.bot == False:
                counter += 1

        await ctx.send(f"Number of users in the server: {counter}")

    @commands.command()
    async def messages(self, ctx, member: discord.Member = None):
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
    async def purge(self, ctx, num: int = 5):
        """Deletes messages in bunches (staff only)"""
        num = 150 if num > 150 else num+1  # sets num to 100 if num is greater than 100
        await ctx.channel.purge(limit=num)

    @commands.command()
    async def rules(self, ctx):
        """What are the rules of this server?"""
        rules = discord.Embed(
            title="Server Rules",
            colour = discord.Colour.dark_gold(),
        )

        rules.add_field(name="Rule 1", value="No racism and polictics", inline=False)
        rules.add_field(name="Rule 2", value="Spamming will result in a kick, mute, or ban", inline=False)
        rules.add_field(name="Rule 3", value="Don't send harmful/malicious content", inline=False)
        rules.add_field(name="Rule 4", value="No NSFW", inline=False)
        rules.add_field(name="Rule 5", value="Only advertise in self-promotion channels", inline=False)
        rules.add_field(name="Rule 6", value=r"Follow discord tos (https://www.discord.com/terms)")
        rules.set_footer(text=f"Requested by: {ctx.author}")
        await ctx.send(embed=rules)

    @commands.command()
    async def cmds(self, ctx):
        """DMs the user all the commands"""
        all_commands = ['```1. kick (staff only)',
                        '2. ban (staff only)',
                        '3. purge (staff only)',
                        '4. messages',
                        '5. members',
                        '6. ping',
                        '7. commands',
                        '8. rules```']

        user = self.bot.get_user(ctx.author.id)
        cmd = '\n'.join(all_commands)
        try:
            await user.send(f"**Commands**:")
            await user.send(f"{cmd}")
            await ctx.send("**Commands were sent in DMs**")
        except Exception:
            await ctx.send(f"**Commands:**"
                           f"{cmd}")

    @commands.command()
    async def info(self, ctx, member: discord.Member=None):
        """User info"""
        member = ctx.author if not member else member
        roles = [role for role in member.roles if role.name != "@everyone"]

        create_date = member.created_at.strftime("%a, %B %#d, %Y, %I:%M:%S %p UTC")
        join_date = member.joined_at.strftime("%a, %B %#d, %Y, %I:%M:%S %p UTC")
        values = []
        values.append(f"\n**Display name**: {member.display_name}")
        values.append(f"\n**Account created on**: {create_date}")
        values.append(f"\n**Joined server on**: {join_date}")
        values.append(f"\n**Roles ({len(roles)})**: " + " ".join([role.mention for role in roles]))
        values.append(f"\n**Bot**: {member.bot}")

        userinfo = discord.Embed(title=f"**{member.display_name}**", colour=discord.Colour.blue(), timestamp=ctx.message.created_at,
                                description=" ".join(values))
        userinfo.set_author(name=f"User Info - {member}", icon_url=member.avatar_url)
        userinfo.set_thumbnail(url=member.avatar_url)
        userinfo.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=userinfo)


