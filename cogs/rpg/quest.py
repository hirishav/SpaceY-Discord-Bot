import discord
from discord.ext import commands
import random
from database import db

class Quest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def quest(self, ctx):
        """Quest commands. (s quest start)"""
        user_id = ctx.author.id
        
        if db.is_on_cooldown(user_id, "quest"):
            cd_time = db.get_cooldown(user_id, "quest")
            remaining = db.format_time_remaining(cd_time)
            await ctx.send(f"Naya quest start karne ke liye **{remaining}** wait karo.")
            return
            
        xp_gained = random.randint(50, 100)
        db.add_xp(user_id, xp_gained)
        db.set_cooldown(user_id, "quest", 6 * 60 * 60) # 6 hours
        
        embed = discord.Embed(
            title=f"{ctx.author.name} — quest",
            description=f"Tumne ek quest pura kiya!\n\n**+{xp_gained}** 🌟 XP",
            color=0x2b2d31
        )
        await ctx.send(embed=embed)

    @quest.command(name="epic")
    async def epic(self, ctx):
        """Epic quest start karo."""
        await ctx.send("Epic quest feature jaldi aayega!")

async def setup(bot):
    await bot.add_cog(Quest(bot))
