import discord
from discord.ext import commands
import random
from database import db

class Vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def vote(self, ctx):
        """Bot ko vote karke inam pao."""
        user_id = ctx.author.id
        
        if db.is_on_cooldown(user_id, "vote"):
            cd_time = db.get_cooldown(user_id, "vote")
            remaining = db.format_time_remaining(cd_time)
            await ctx.send(f"Aapne already vote kar diya hai! **{remaining}** wait karo.")
            return
            
        coins_gained = random.randint(1000, 3000)
        db.add_coins(user_id, coins_gained)
        
        db.set_cooldown(user_id, "vote", 12 * 60 * 60) # 12 hours
        
        embed = discord.Embed(
            title=f"{ctx.author.name} — vote",
            description=f"Vote karne ke liye shukriya!\n\n**+{coins_gained}** 🟡 coins",
            color=0x2b2d31
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Vote(bot))
