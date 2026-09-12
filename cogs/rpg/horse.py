import discord
from discord.ext import commands

class Horse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def horse(self, ctx):
        """Apne ghode ka status dekho."""
        embed = discord.Embed(
            title=f"{ctx.author.name} ka Ghoda",
            description="Abhi tumhare paas **Tier 1** ka normal ghoda hai 🐎\n\nIska naam rakhne ke liye ya isko feed karne ka system abhi under development hai!",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Horse(bot))