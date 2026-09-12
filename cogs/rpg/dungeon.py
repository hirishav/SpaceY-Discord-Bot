import discord
from discord.ext import commands
from database import db

class Dungeon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dungeon(self, ctx):
        """Dungeon me enter karo (agar key hai to)."""
        user_id = ctx.author.id
        user = db.get_user(user_id)
        
        # Check if user has a dungeon key (placeholder logic)
        keys = user["inventory"].get("dungeon key", 0)
        
        if keys > 0:
            db.add_item(user_id, "dungeon key", -1)
            embed = discord.Embed(
                title=f"⚔️ {ctx.author.name} Dungeon me ghus gaya!",
                description="Tumne ek `🗝️ dungeon key` use kiya aur dark dungeon me enter kiya...\n\n(Dungeon fighting system under development hai!)",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("Tumhare paas **🗝️ dungeon key** nahi hai! Pehle shop se kharid ke aao. 😅")

async def setup(bot):
    await bot.add_cog(Dungeon(bot))