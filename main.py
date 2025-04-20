import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables from .env file
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents,
                   application_id='1029161693625991175')


@bot.event
async def on_ready():
    print('Logged in.')


async def load():
    bot.remove_command('help')
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            cog_name = f'cogs.{file[:-3]}'
            try:
                await bot.load_extension(cog_name)
                print(f"Loaded cog: {cog_name}")
            except Exception as e:
                print(f"Failed to load cog: {cog_name} | {e}")


async def main():
    await load()
    # Load token from .env
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise ValueError("DISCORD_TOKEN is not set in the .env file")
    await bot.start(token)

asyncio.run(main())

# to do:
# turn commands into slash command variation (DONE)
# display a link after searching (DONE)
# maybe search output to being an embed - reason: can take up to 6000 characters collectively instead of just 2k in a normal discord message, 4k limit fix this lol
# replace the !help command to display parameter inputs, easier for user (DONE)
# use cogs, clean up code (DONE)
# work on potential edge cases that pop up
# weather searching functionality
# datetime / timezone checker
# potentially a google search
# potentially a youtube search
# potentially a github search
# potentially a spotify search
# potentially a twitch search
# potentially bard bot functionality
