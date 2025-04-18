import discord
from discord.ext import commands

class Sync(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="sync")
    @commands.is_owner()
    async def sync(self, ctx: commands.Context):
        try:
            synced = await self.bot.tree.sync()
            await ctx.send(f"Synced {len(synced)} command(s)!")
        except Exception as e:
            await ctx.send("Failed to sync commands.")
            print(e)

async def setup(bot: commands.Bot):
    await bot.add_cog(Sync(bot))