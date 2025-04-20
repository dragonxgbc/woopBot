import discord
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Help",
            description="Below is a list of available commands:",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="search",
            value=(
                "Search Wikipedia by title. "
                "Usage: `!search <query>` or `/search <query>`\n\n"
                "This command fetches the Wikipedia summary for the given query. "
                "If the summary exceeds 4096 characters, it's split into multiple pages "
                "with navigation buttons."
            ),
            inline=False
        )
        await ctx.send(embed=embed)

    @discord.app_commands.command(name="help", description="Display available commands")
    async def help_slash(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Help",
            description="Below is a list of available commands:",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="search",
            value=(
                "Search Wikipedia by title. "
                "Usage: `/search <query>`\n\n"
                "This command fetches the Wikipedia summary for the given query. "
                "If the summary exceeds 4096 characters, it is split into multiple pages "
                "with navigation buttons."
            ),
            inline=False
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(HelpCog(bot))