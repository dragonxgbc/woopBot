import discord
from discord.ext import commands

class HelpCog(commands.Cog):
    COMMAND_INFO = {
        "search": {
            "description": (
                "Search Wikipedia by title.\n"
                "Fetches the Wikipedia summary for the given query. "
                "If the summary exceeds 4096 characters, it will be split into pages with navigation buttons."
            ),
            "usage": {"prefix": "!search <query>", "slash": "/search <query>"}
        },
        "checktime": {
            "description": (
                "Check the current date & time in major timezones.\n"
                "Displays 24-hour and 12-hour formats for key timezones."
            ),
            "usage": {"prefix": "!checktime", "slash": "/checktime"}
        }
    }

    def __init__(self, bot: commands.Bot):
        # Remove default help to avoid duplicate outputs
        bot.remove_command('help')
        self.bot = bot

    def _build_help_embed(self, is_slash: bool) -> discord.Embed:
        embed = discord.Embed(
            title="Help",
            description="Below is a list of available commands:",
            color=discord.Color.blue()
        )
        for cmd_name, info in self.COMMAND_INFO.items():
            usage = info["usage"]["slash" if is_slash else "prefix"]
            field_value = f"{info['description']}\nUsage: `{usage}`"
            embed.add_field(name=cmd_name, value=field_value, inline=False)
        return embed

    @commands.command(name="help")
    async def help_command(self, ctx: commands.Context):
        """Show help via prefix command"""
        embed = self._build_help_embed(is_slash=False)
        await ctx.send(embed=embed)

    @discord.app_commands.command(name="help", description="Display available commands")
    async def help_slash(self, interaction: discord.Interaction):
        """Show help via slash command"""
        embed = self._build_help_embed(is_slash=True)
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(HelpCog(bot))
