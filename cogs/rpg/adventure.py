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
            
        xp_gained = random.randint(3000, 7000)
        coins_gained = random.randint(100, 500)
        
        db.set_cooldown(user_id, "adventure", 1 * 60 * 60) # 1 hour
        
        success = random.choice([True, False])
        
        mobs = [
            ("🧟", "CYCLOPS"),
            ("🐉", "DRAGON"),
            ("👹", "OGRE"),
            ("👺", "GOBLIN")
        ]
        emoji, mob_name = random.choice(mobs)
        
        if success:
            db.add_xp(user_id, xp_gained)
            db.add_coins(user_id, coins_gained)
            msg = f"**{ctx.author.name}** found and killed a {emoji} **{mob_name}**\n"
            msg += f"Earned {coins_gained:,} coins and {xp_gained:,} XP\n"
            await ctx.send(msg)
        else:
            msg = f"**{ctx.author.name}** found a {emoji} **{mob_name}**, but lost fighting\n"
            msg += "**Your horse** saved you before the enemy kills you"
            await ctx.send(msg)

async def setup(bot):
    await bot.add_cog(Adventure(bot))
