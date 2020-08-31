from discord.ext import commands
import discord


def setup(bot):
    bot.add_cog(Challenges(bot=bot))


class Challenges(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.channel.id == 749648051613728879:
            submitted = message.guild.get_role(749700088292573204)
            solutions = message.guild.get_channel(749648303808839691)
            if submitted not in message.author.roles:
                await message.delete()
                if message.content.count("```") != 2:
                    msg = f"{message.author.mention} make sure to submit in a code " \
                          f"block and only include the code required for the challenge!"
                    return await message.channel.send(msg, delete_after=10.0)
                await message.author.add_roles(submitted)
                embed = discord.Embed(description=message.content, color=message.guild.me.top_role.color)
                embed.set_author(name=str(message.author), icon_url=message.author.avatar_url)
                embed.set_footer(text=f'#ID: {message.author.id}')
                await solutions.send(embed=embed)
