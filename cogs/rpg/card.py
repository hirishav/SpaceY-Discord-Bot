import discord
from discord.ext import commands
import random
from database import db

class Card(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def card(self, ctx):
        """Cards ke related commands."""
        await ctx.send("Type `s card hand` to see your hand.")

    @card.command(name="hand")
    async def hand(self, ctx):
        """Apne cards dekho."""
        user_id = ctx.author.id
        
        if db.is_on_cooldown(user_id, "card_hand"):
            cd_time = db.get_cooldown(user_id, "card_hand")
            remaining = db.format_time_remaining(cd_time)
            await ctx.send(f"Thoda sabar karo! **{remaining}** wait karo.")
            return
            
        db.set_cooldown(user_id, "card_hand", 1 * 60 * 60) # 1 hour
        
        embed = discord.Embed(
            title=f"{ctx.author.name} — card hand",
            description=f"Yeh rahe tumhare cards!\n(Cards ka feature jaldi aayega)",
            color=0x2b2d31
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Card(bot))
