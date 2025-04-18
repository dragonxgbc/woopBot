import discord
from discord.ext import commands
import wikipedia
import requests  # Still imported if you use it elsewhere

# Pagination view for navigating long summaries
class WikiPaginationView(discord.ui.View):
    def __init__(self, pages: list[str], title: str, url: str):
        super().__init__()
        # Make sure each page has spaced paragraphs.
        self.pages = [page.replace("\n", "\n\n") for page in pages]
        self.current_page = 0
        self.title = title
        self.url = url

    def create_embed(self) -> discord.Embed:
        # Append the "Read More" link to each page.
        description = self.pages[self.current_page] + f"\n\n[Read More]({self.url})"
        embed = discord.Embed(title=self.title, description=description)
        embed.set_footer(text=f"Page {self.current_page + 1}/{len(self.pages)}")
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

class SearchCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def lookup_page(self, query: str) -> wikipedia.WikipediaPage:
        """
        Attempts to look up a page by title (with auto_suggest turned off).
        If the page isn't found or is ambiguous, it falls back to a normal search.
        """
        try:
            # Try to look up the page using the exact title.
            return wikipedia.page(query, auto_suggest=False)
        except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError):
            # Fall back to searching for the query if the exact match is not found.
            results = wikipedia.search(query, results=5)
            if not results:
                raise wikipedia.exceptions.PageError(f"No results found for '{query}'.")
            return wikipedia.page(results[0], auto_suggest=False)

    # Slash command version (title lookup only with fallback to search)
    @discord.app_commands.command(name="search", description="Search Wikipedia for a topic by title.")
    async def search(self, interaction: discord.Interaction, query: str):
        try:
            page = self.lookup_page(query)
            summary = page.summary  # full summary text
            title = page.title
            url = page.url

            # Replace single newlines with double newlines for spacing
            formatted_summary = summary.replace("\n", "\n\n")

            if len(formatted_summary) > 6000:
                pages = [formatted_summary[i:i+6000] for i in range(0, len(formatted_summary), 6000)]
                embed = discord.Embed(title=title, description=pages[0] + f"\n\n[Read More]({url})")
                embed.set_footer(text=f"Page 1/{len(pages)}")
                view = WikiPaginationView(pages, title, url)
                await interaction.response.send_message(embed=embed, view=view)
            else:
                embed = discord.Embed(title=title, description=formatted_summary + f"\n\n[Read More]({url})")
                await interaction.response.send_message(embed=embed)
        except Exception as exc:
            await interaction.response.send_message("An error occurred while fetching the Wikipedia summary.")
            print(exc)

    # Prefix command version (triggered by !search; title lookup only with fallback to search)
    @commands.command(name="search")
    async def search_prefix(self, ctx: commands.Context, *, query: str):
        try:
            page = self.lookup_page(query)
            summary = page.summary  # full summary text
            title = page.title
            url = page.url

            # Replace single newlines with double newlines for spacing
            formatted_summary = summary.replace("\n", "\n\n")

            if len(formatted_summary) > 6000:
                pages = [formatted_summary[i:i+6000] for i in range(0, len(formatted_summary), 6000)]
                embed = discord.Embed(title=title, description=pages[0] + f"\n\n[Read More]({url})")
                embed.set_footer(text=f"Page 1/{len(pages)}")
                view = WikiPaginationView(pages, title, url)
                await ctx.send(embed=embed, view=view)
            else:
                embed = discord.Embed(title=title, description=formatted_summary + f"\n\n[Read More]({url})")
                await ctx.send(embed=embed)
        except Exception as exc:
            await ctx.send("An error occurred while fetching the Wikipedia summary.")
            print(exc)

async def setup(bot: commands.Bot):
    await bot.add_cog(SearchCog(bot))