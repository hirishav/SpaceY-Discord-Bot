import discord
from discord.ext import commands
import random
from database import db

class Rewards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def daily(self, ctx):
        """Rozana ka inam claim karo!"""
        user_id = ctx.author.id
        
        if db.is_on_cooldown(user_id, "daily"):
            cd_time = db.get_cooldown(user_id, "daily")
            remaining = db.format_time_remaining(cd_time)
            await ctx.send(f"Bhai thoda sabar karo! Agla daily inam **{remaining}** ke baad milega. 😅")
            return
            
        # Give rewards
        coins_gained = random.randint(1000, 5000)
        db.add_coins(user_id, coins_gained)
        
        # Add some potions randomly
        potions = random.randint(1, 3)
        db.add_item(user_id, "life potion", potions)
        
        # Set 24 hour cooldown
        db.set_cooldown(user_id, "daily", 24 * 60 * 60)
        
        embed = discord.Embed(
            title=f"{ctx.author.name} — Daily Inam",
            description=f"Tumhe Area #1 ke rewards mil gaye!\n\n**+{coins_gained}** 🟡 coins\n**+{potions}** 🩸 life potion\n\nRoz aana mat bhulna!",
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def weekly(self, ctx):
        """Hafte ka bada inam claim karo!"""
        user_id = ctx.author.id
        
        if db.is_on_cooldown(user_id, "weekly"):
            cd_time = db.get_cooldown(user_id, "weekly")
            remaining = db.format_time_remaining(cd_time)
            await ctx.send(f"Aram se bhai! Agla weekly inam **{remaining}** ke baad claim kar sakte ho. 😅")
            return
            
        # Give rewards
        coins_gained = random.randint(20000, 50000)
        db.add_coins(user_id, coins_gained)
        
        db.add_item(user_id, "rare lootbox", 2)
        
        # Set 7 days cooldown
        db.set_cooldown(user_id, "weekly", 7 * 24 * 60 * 60)
        
        embed = discord.Embed(
            title=f"{ctx.author.name} — Weekly Inam",
            description=f"Waah! Area #1 ke weekly rewards mil gaye!\n\n**+{coins_gained}** 🟡 coins\n**+2** 📦 rare lootbox\n\nAb agle hafte milte hain!",
            color=discord.Color.magenta()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Rewards(bot))