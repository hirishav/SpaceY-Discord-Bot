import discord
from discord.ext import commands
import random
from database import db

class Hunt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hunt(self, ctx):
        """Jungle me shikaar karo aur XP kamao."""
        user_id = ctx.author.id
        
        if db.is_on_cooldown(user_id, "hunt"):
            cd_time = db.get_cooldown(user_id, "hunt")
            remaining = db.format_time_remaining(cd_time)
            await ctx.send(f"Abhi hunt par nahi jaa sakte! **{remaining}** wait karo.")
            return
            
        xp_gained = random.randint(15, 35)
        coins_gained = random.randint(5, 20)
        
        db.add_xp(user_id, xp_gained)
        db.add_coins(user_id, coins_gained)
        
        db.set_cooldown(user_id, "hunt", 1 * 60) # 1 minute
        
        embed = discord.Embed(
            title=f"{ctx.author.name} — hunt",
            description=f"Tum jungle gaye aur shikaar kiya!\n\n**+{xp_gained}** 🌟 XP\n**+{coins_gained}** 🟡 coins",
            color=0x2b2d31
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Hunt(bot))
