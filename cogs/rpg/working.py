import discord
from discord.ext import commands
import random
from database import db

class Working(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _handle_working(self, ctx, action_name):
        user_id = ctx.author.id
        
        if db.is_on_cooldown(user_id, "working"):
            cd_time = db.get_cooldown(user_id, "working")
            remaining = db.format_time_remaining(cd_time)
            await ctx.send(f"Abhi thak gaye ho! Agla kaam **{remaining}** baad karna.")
            return
            
        items = ["log", "fish", "apple", "iron"]
        item_found = random.choice(items)
        amount = random.randint(1, 3)
        
        db.add_item(user_id, item_found, amount)
        db.set_cooldown(user_id, "working", 5 * 60) # 5 minutes cooldown shared across all working commands
        
        embed = discord.Embed(
            title=f"{ctx.author.name} — {action_name}",
            description=f"Tumne {action_name} kiya aur kuch mila!\n\n**+{amount}** {item_found}",
            color=0x2b2d31
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def chop(self, ctx):
        await self._handle_working(ctx, "chop")

    @commands.command()
    async def fish(self, ctx):
        await self._handle_working(ctx, "fish")

    @commands.command()
    async def pickup(self, ctx):
        await self._handle_working(ctx, "pickup")

    @commands.command()
    async def mine(self, ctx):
        await self._handle_working(ctx, "mine")

async def setup(bot):
    await bot.add_cog(Working(bot))
