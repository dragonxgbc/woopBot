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
                "Search Wikipedia by title.\n"
                "Usage: `!search <query>` or `/search <query>`\n\n"
                "Fetches the Wikipedia summary for the given query. If the summary exceeds 4096 characters, "
                "it will be split into multiple pages with navigation buttons."
            ),
            inline=False
        )
        embed.add_field(
            name="time",
            value=(
                "Check the current date & time in major timezones.\n"
                "Usage: `!time` or `/time`\n\n"
                "Displays the current date and time in both 24-hour and 12-hour (AM/PM) formats for key timezones."
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
                "Search Wikipedia by title.\n"
                "Usage: `/search <query>`\n\n"
                "Fetches the Wikipedia summary for the given query. If the summary exceeds 4096 characters, "
                "it will be split into multiple pages with navigation buttons."
            ),
            inline=False
        )
        embed.add_field(
            name="time",
            value=(
                "Check the current date & time in major timezones.\n"
                "Usage: `/time`\n\n"
                "Displays the current date and time in both 24-hour and 12-hour (AM/PM) formats for key timezones."
            ),
            inline=False
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(HelpCog(bot))