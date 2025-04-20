import datetime
import discord
from discord.ext import commands
from zoneinfo import ZoneInfo

class TimePaginationView(discord.ui.View):
    def __init__(self, pages: list[list[tuple[str, str]]], title: str = "Current Date & Time in Major Timezones"):
        super().__init__(timeout=None)
        self.pages = pages
        self.title = title
        self.page_idx = 0

    def create_embed(self) -> discord.Embed:
        embed = discord.Embed(title=self.title, color=discord.Color.green())
        for name, value in self.pages[self.page_idx]:
            embed.add_field(name=name, value=value, inline=False)
        embed.set_footer(text=f"Page {self.page_idx + 1}/{len(self.pages)}")
        return embed

    async def _turn_page(self, interaction: discord.Interaction, delta: int):
        self.page_idx = (self.page_idx + delta) % len(self.pages)
        await interaction.response.edit_message(embed=self.create_embed(), view=self)

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._turn_page(interaction, -1)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._turn_page(interaction, 1)

class TimeCog(commands.Cog):
    # Preinstantiate ZoneInfo objects and static groups
    TIMEZONES = {
        name: ZoneInfo(location) for name, location in {
            "UTC": "UTC",
            "US Eastern": "US/Eastern",
            "US Central": "US/Central",
            "US Mountain": "US/Mountain",
            "US Pacific": "US/Pacific",
            "London": "Europe/London",
            "Berlin": "Europe/Berlin",
            "Tokyo": "Asia/Tokyo",
            "Dubai": "Asia/Dubai",
            "Kolkata": "Asia/Kolkata",
            "Sydney": "Australia/Sydney",
        }.items()
    }
    GROUPS = [
        ["UTC", "US Eastern", "US Central", "US Mountain", "US Pacific"],
        [name for name in TIMEZONES if name not in (
            "UTC", "US Eastern", "US Central", "US Mountain", "US Pacific"
        )]
    ]

    @staticmethod
    def _format_time(dt: datetime.datetime) -> str:
        return dt.strftime("%Y-%m-%d\n24-hour: %H:%M:%S\n12-hour: %I:%M:%S %p")

    def _make_pages(self) -> list[list[tuple[str, str]]]:
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        return [
            [
                (tz, self._format_time(now_utc.astimezone(self.TIMEZONES[tz])))
                for tz in group
            ]
            for group in self.GROUPS
        ]

    async def _send_paginated(self, send_func):
        pages = self._make_pages()
        view = TimePaginationView(pages)
        await send_func(embed=view.create_embed(), view=view)

    @commands.command(name="time")
    async def time_command(self, ctx: commands.Context):
        await self._send_paginated(ctx.send)

    @discord.app_commands.command(name="time", description="Check current date & time split by US/International zones")
    async def time_slash(self, interaction: discord.Interaction):
        await self._send_paginated(interaction.response.send_message)

async def setup(bot: commands.Bot):
    await bot.add_cog(TimeCog(bot))
