import discord
from discord.ext import commands

class Horse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def horse(self, ctx):
        """Apne ghode ka status dekho."""
        embed = discord.Embed(
            title="Stable",
            description="> Tumhara wafadar aur pyara ghoda yahan aaram kar raha hai. 🌾\n\n**Tier:** `1`\n**Type:** `Normal` 🐎\n\n*Naam rakhne aur feed karne ka system jald hi aa raha hai!*",
            color=discord.Color.dark_orange()
        )
        embed.set_author(name=f"{ctx.author.display_name}'s Horse", icon_url=ctx.author.display_avatar.url if ctx.author.display_avatar else None)
        embed.set_thumbnail(url="https://images.emojiterra.com/twitter/v14.0/512px/1f40e.png")
        embed.set_footer(text="SpaceY RPG • Horse Menu")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Horse(bot))