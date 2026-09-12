import discord
from discord.ext import commands
import random
from database import db

class Training(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['tr'])
    async def training(self, ctx):
        """Apne skills ko train karo."""
        user_id = ctx.author.id
        
        if db.is_on_cooldown(user_id, "training"):
            cd_time = db.get_cooldown(user_id, "training")
            remaining = db.format_time_remaining(cd_time)
            await ctx.send(f"Training ke baad thakan hoti hai! **{remaining}** aaram karo.")
            return
            
        xp_gained = random.randint(10, 25)
        
        db.add_xp(user_id, xp_gained)
        db.set_cooldown(user_id, "training", 15 * 60) # 15 minutes
        
        embed = discord.Embed(
            title=f"{ctx.author.name} — training",
            description=f"Kadi mehnat ke baad...\n\n**+{xp_gained}** 🌟 XP",
            color=0x2b2d31
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Training(bot))
