import discord
from discord.ext import commands
import random
from database import db

class Adventure(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['adv'])
    async def adventure(self, ctx):
        """Adventure par jao."""
        user_id = ctx.author.id
        
        if db.is_on_cooldown(user_id, "adventure"):
            cd_time = db.get_cooldown(user_id, "adventure")
            remaining = db.format_time_remaining(cd_time)
            await ctx.send(f"Naye adventure ke liye taiyar nahi ho. **{remaining}** wait karo.")
            return
            
        xp_gained = random.randint(30, 70)
        coins_gained = random.randint(10, 50)
        
        db.add_xp(user_id, xp_gained)
        db.add_coins(user_id, coins_gained)
        
        db.set_cooldown(user_id, "adventure", 1 * 60 * 60) # 1 hour
        
        embed = discord.Embed(
            title=f"{ctx.author.name} — adventure",
            description=f"Ek lamba adventure poora hua!\n\n**+{xp_gained}** 🌟 XP\n**+{coins_gained}** 🟡 coins",
            color=0x2b2d31
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Adventure(bot))
