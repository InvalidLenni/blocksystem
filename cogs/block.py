import sqlite3

import discord
from discord.ext import commands


class Block(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="ban", description="Ban a user", options=[
        discord.Option("userid", description="The ID of the user you want to ban", required=True, type=int),
        discord.Option("reason", description="The reason for the ban", required=True, type=str)
    ])
    @commands.is_owner()
    async def _ban(self, ctx, userid, reason):
        if ctx.author.bot:
            return
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel FROM log WHERE guild = {ctx.guild.id}")
        result = cursor.fetchone()
        user = await self.bot.fetch_user(userid)
        member = user
        channel = self.bot.get_channel(906221245962539069)
        embed2 = discord.Embed(title="Log | Ban",
                               description=f'Moderator: {ctx.author} | {ctx.author.id}\nNew banned user: {member} | {member.id}\nReason: {reason}',
                               color=discord.Color.red())
        embed = discord.Embed(title="Blocked",
                              description=f"I've now {member.mention} banned on 4 different servers . (ID: {member.id})")
        embed3 = discord.Embed(title="Blocked",
                               description=f'Hello, you was banned on multiple server from BlockSystem. The Reason for this is {reason}\nModerator: {ctx.author.mention}\n\nYou can submit a ban request on our [support server](https://discord.gg/5zRU7wZKSa).')
        for guild in self.bot.guilds:
            await guild.ban(member, reason=f"BannSystem Ban | Reason: {reason}\nModerator: {ctx.author}")
        for i, x in enumerate(result, 1):
            await x.send(embed=embed2)
        await channel.send(embed=embed2)
        await member.send(embed=embed3)
        await ctx.send(embed=embed, hidden=True)


def setup(bot):
    bot.add_cog(Block(bot))
