import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables from .env file
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
application_id = os.getenv("APPLICATION_ID")
if not application_id:
    raise ValueError("APPLICATION_ID is not set in the .env file")

bot = commands.Bot(command_prefix='!', intents=intents, application_id=application_id)


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
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise ValueError("DISCORD_TOKEN is not set in the .env file")
    await bot.start(token)

asyncio.run(main())

# done:
# added slash commands
# finished search command
# finished help command

# to do:
# work on potential edge cases that pop up
# weather searching functionality
# datetime / timezone checker

# optional:
# a google search
# a youtube search
# a github search
# a spotify search
# a twitch search
# ai integration
