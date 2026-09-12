import discord
from discord.ext import commands

class Heal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def heal(self, ctx):
        """Heal your life."""
        await ctx.send(f"**{ctx.author.name}**, your life has been restored")

async def setup(bot):
    await bot.add_cog(Heal(bot))
