import sqlite3

import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option


class Block(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="setlog",
        description="Set the log for the new blocksystem bans. (Required: ID in the whitelist database)",
        options=[
            create_option(
                name="channel",
                description="Please enter the channel for the blocksystem ban log.",
                option_type=6,
                required=True
            )
        ])
    @commands.is_owner()
    async def setlog(self, ctx, channel: discord.TextChannel):
        if ctx.author.bot:
            return
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel FROM log WHERE guild = {ctx.guild.id}")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO log(guild, channel) VALUES(?,?)")
            val = (ctx.guild.id, channel.id)
            embed = discord.Embed(title="logchannel is now been set",
                                  description=f'the logchannel has now been set to {channel.mention}.',
                                  color=discord.Color.red())
            await ctx.send(embed=embed, hidden=True)
            await channel.send(embed=embed)
            cursor.execute(sql, val)
            db.commit()
        elif result is not None:
            embed = discord.Embed(title="already set",
                                  description="The logchannel is already set, you can remove the logchannel with ``/removelog``.",
                                  color=discord.Color.red())
            await ctx.send(embed=embed, hidden=True)
        cursor.close()
        db.close()

    @cog_ext.cog_slash(
        name="removelog",
        description="Remove the log for the new blocksystem bans. (Required: ID in the whitelist database)",
        options=[
            create_option(
                name="channel",
                description="Please enter the channel for the blocksystem ban log.",
                option_type=6,
                required=True
            )
        ])
    @commands.is_owner()
    async def removelog(self, ctx, channel: discord.TextChannel):
        if ctx.author.bot:
            return
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel FROM log WHERE guild = {ctx.guild.id}")
        result = cursor.fetchone()
        if result is None:
            embed = discord.Embed(title="Error",
                                  description=f'the logchannel was not set, you can set the logchannel with ``/setlog``.',
                                  color=discord.Color.red())
            await ctx.send(embed=embed, hidden=True)
            await channel.send(embed=embed, hidden=True)
        elif result is not None:
            sql = (f"DELETE FROM log WHERE channel = {channel.id} AND guild = {ctx.guild.id}")
            embed = discord.Embed(title="logchannel removed",
                                  description="The logchannel is now removed, you can add the logchannel with ``/setlog`` again.",
                                  color=discord.Color.red())
            await ctx.send(embed=embed, hidden=True)
            cursor.execute(sql)
            db.commit()
        cursor.close()
        db.close()


def setup(bot):
    bot.add_cog(Block(bot))
