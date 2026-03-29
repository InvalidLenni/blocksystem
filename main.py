import asyncio
import sys


import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="b!")
bot.remove_command('help')

@bot.event
async def on_():
    print("Online")





initial_extensions = ['cogs.block', 'cogs.unblock', 'cogs.log']

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            print(f'Ich habe {extension} geladen!')
        except Exception as e:
            print(f'Ich konnte nicht {extension} laden!', file=sys.stderr)

bot.run("YOUR BOT TOKEN")
