import discord
from discord.ext import commands
import wikipedia
import re

# Precompile regex for performance
_SPACING_REGEX = re.compile(r"\n+")

class WikiPaginationView(discord.ui.View):
    def __init__(self, pages: list[str], title: str, url: str):
        super().__init__()
        # normalize spacing once, using precompiled regex
        self.pages = [_SPACING_REGEX.sub("\n\n", page) for page in pages]
        self.current_page = 0
        self.title = title
        self.url = url

    def create_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title=self.title,
            url=self.url,
            description=self.pages[self.current_page]
        )
        # Footer now only shows page info
        footer = f"Page {self.current_page + 1}/{len(self.pages)}"
        embed.set_footer(text=footer)
        return embed

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
        await interaction.response.edit_message(embed=self.create_embed(), view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
        await interaction.response.edit_message(embed=self.create_embed(), view=self)


def split_summary(summary: str, limit: int = 4096) -> list[str]:
    if "\n" not in summary:
        return [summary]

    paragraphs = summary.split("\n")
    pages: list[str] = []
    current: list[str] = []
    for para in paragraphs:
        cand = "\n".join(current + [para])
        if len(cand) > limit:
            if current:
                pages.append("\n".join(current))
                current = [para]
            else:
                # chunk long paragraph
                while len(para) > limit:
                    pages.append(para[:limit])
                    para = para[limit:]
                current = [para]
        else:
            current.append(para)

    if current:
        pages.append("\n".join(current))
    return pages

class SearchCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def lookup_page(self, query: str) -> wikipedia.WikipediaPage:
        try:
            return wikipedia.page(query, auto_suggest=False)
        except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError):
            results = wikipedia.search(query, results=5)
            if not results:
                raise wikipedia.exceptions.PageError(f"No results for '{query}'.")
            return wikipedia.page(results[0], auto_suggest=False)

    async def _send(self, responder, summary: str, title: str, url: str):
        pages = split_summary(summary)
        view = WikiPaginationView(pages, title, url)
        embed = view.create_embed()
        # send with view only if multiple pages
        if len(pages) > 1:
            await responder(embed=embed, view=view)
        else:
            await responder(embed=embed)

    @discord.app_commands.command(name="search", description="Search Wikipedia by title.")
    async def search(self, interaction: discord.Interaction, query: str):
        try:
            page = self.lookup_page(query)
            await self._send(
                interaction.response.send_message,
                page.summary, page.title, page.url
            )
        except Exception as exc:
            await interaction.response.send_message("Error fetching Wikipedia summary.")
            print(exc)

    @commands.command(name="search")
    async def search_prefix(self, ctx: commands.Context, *, query: str):
        try:
            page = self.lookup_page(query)
            # wrap ctx.send so it matches responder interface
            await self._send(ctx.send, page.summary, page.title, page.url)
        except Exception as exc:
            await ctx.send("Error fetching Wikipedia summary.")
            print(exc)

async def setup(bot: commands.Bot):
    await bot.add_cog(SearchCog(bot))