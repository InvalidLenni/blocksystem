import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option


class Unblock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="unblock",
        description="Unblock a blocksystem banned user. (Only owner actually)",
        options=[
            create_option(
                name="userid",
                description="Please enter the userid.",
                option_type=3,
                required=True
            )
    ])
    @commands.is_owner()
    async def unblock(self, ctx, userid):
        if ctx.author.bot:
            return
        user = await self.bot.fetch_user(userid)
        member = user
        channel = self.bot.get_channel(906221245962539069)
        embed2 = discord.Embed(title="Log | Unblock", description=f'Moderator: {ctx.author} | {ctx.author.id}\nUnbanned user: {member.id} | {member.mention}',
                               color=discord.Color.green())
        embed = discord.Embed(title="Unblocked",
                              description=f"I've now {member.mention} unbanned on 5 different servers. (ID: {member.id})")
        await ctx.send(embed=embed, hidden=True)
        for guild in self.bot.guilds:
            await guild.unban(user, reason=f'BlockSystem Unban | Penalty canceled | Moderator: {ctx.author.name}')
        await channel.send(embed=embed2)


def setup(bot):
    bot.add_cog(Unblock(bot))
