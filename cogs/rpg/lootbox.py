import discord
from discord.ext import commands
import random
from database import db

class Lootbox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def lootbox(self, ctx):
        """Lootbox open karo."""
        user_id = ctx.author.id
        
        if db.is_on_cooldown(user_id, "lootbox"):
            cd_time = db.get_cooldown(user_id, "lootbox")
            remaining = db.format_time_remaining(cd_time)
            await ctx.send(f"Lootbox abhi available nahi hai! **{remaining}** wait karo.")
            return
            
        coins_gained = random.randint(500, 1500)
        db.add_coins(user_id, coins_gained)
        
        db.set_cooldown(user_id, "lootbox", 3 * 60 * 60) # 3 hours
        
        embed = discord.Embed(
            title=f"{ctx.author.name} — lootbox",
            description=f"Tumne ek lootbox khola!\n\n**+{coins_gained}** 🟡 coins",
            color=0x2b2d31
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Lootbox(bot))
