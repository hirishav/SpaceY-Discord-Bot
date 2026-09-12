import discord
from discord.ext import commands
import random
from database import db

class Duel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def duel(self, ctx, member: discord.Member = None):
        """Dusre player se ladaai karo."""
        user_id = ctx.author.id
        
        if db.is_on_cooldown(user_id, "duel"):
            cd_time = db.get_cooldown(user_id, "duel")
            remaining = db.format_time_remaining(cd_time)
            await ctx.send(f"Aap abhi duel nahi kar sakte! **{remaining}** wait karo.")
            return
            
        if not member or member == ctx.author:
            await ctx.send("Kisse ladna hai? Kisine mention karo: `s duel @user`")
            return
            
        xp_gained = random.randint(20, 50)
        db.add_xp(user_id, xp_gained)
        db.set_cooldown(user_id, "duel", 2 * 60 * 60) # 2 hours
        
        embed = discord.Embed(
            title=f"{ctx.author.name} — duel",
            description=f"Tumne {member.name} se duel kiya aur jeet gaye!\n\n**+{xp_gained}** 🌟 XP",
            color=0x2b2d31
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Duel(bot))
