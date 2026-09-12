import discord
from discord.ext import commands
from database import db

class Heal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def heal(self, ctx):
        """Heal your life using a life potion."""
        user_id = ctx.author.id
        potions = db.get_item_amount(user_id, "life potion")
        
        if potions <= 0:
            await ctx.send(f"**{ctx.author.name}**, tumhare paas koi `life potion` nahi hai! ❌")
            return
            
        user_data = db.get_user_all(user_id)
        if not user_data:
            db.add_coins(user_id, 0)
            user_data = db.get_user_all(user_id)
            
        hp = user_data['hp']
        max_hp = user_data['max_hp']
        
        if hp >= max_hp:
            await ctx.send(f"**{ctx.author.name}**, tumhari health pehle se hi full hai! ❤️")
            return
            
        # Deduct 1 potion
        db.add_item(user_id, "life potion", -1)
        
        # Restore HP
        db.set_hp(user_id, max_hp)
        
        embed = discord.Embed(
            description=f"✅ **{ctx.author.name}**, you drank a **life potion**! Your life has been fully restored.\n> ❤️ **LIFE:** {max_hp}/{max_hp}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Heal(bot))
