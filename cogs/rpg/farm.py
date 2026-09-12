import discord
from discord.ext import commands
import random
from database import db

class Farm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def farm(self, ctx):
        """Kheti karo aur XP/items kamao!"""
        user_id = ctx.author.id
        
        if db.is_on_cooldown(user_id, "farm"):
            cd_time = db.get_cooldown(user_id, "farm")
            remaining = db.format_time_remaining(cd_time)
            await ctx.send(f"Zameen abhi tyaar nahi hai. **{remaining}** baad wapas aana kheti karne! 🌾")
            return
            
        # Give rewards
        xp_gained = random.randint(100, 500)
        db.add_xp(user_id, xp_gained)
        
        carrots = random.randint(3, 8)
        db.add_item(user_id, "carrot", carrots)
        
        # Set 10 mins cooldown
        db.set_cooldown(user_id, "farm", 10 * 60)
        
        await ctx.send(f"{ctx.author.name} ne zameen me 🥕 seed boya...\n**{carrots} 🥕 carrot** ug gaye!\nEarned {xp_gained} XP ✨")

async def setup(bot):
    await bot.add_cog(Farm(bot))