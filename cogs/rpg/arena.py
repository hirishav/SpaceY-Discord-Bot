import discord
from discord.ext import commands

class Arena(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def arena(self, ctx):
        """PvP Arena me doosre players se lado!"""
        embed = discord.Embed(
            title=f"🛡️ PvP Arena",
            description=f"{ctx.author.name} arena me utar chuka hai!\n\n(Arena ka PvP matchmaking aur fighting system abhi ban raha hai. Jaldi hi aayega!)",
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Arena(bot))