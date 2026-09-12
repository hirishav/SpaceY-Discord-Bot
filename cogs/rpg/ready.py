import discord
from discord.ext import commands
import time
from database import db

class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['rd'])
    async def ready(self, ctx):
        """Dikhaata hai kaun kaun se commands ready hain."""
        user_id = ctx.author.id
        
        # Check cooldowns
        lootbox = not db.is_on_cooldown(user_id, "lootbox")
        card_hand = not db.is_on_cooldown(user_id, "card_hand")
        vote = not db.is_on_cooldown(user_id, "vote")
        hunt = not db.is_on_cooldown(user_id, "hunt")
        adventure = not db.is_on_cooldown(user_id, "adventure")
        training = not db.is_on_cooldown(user_id, "training")
        duel = not db.is_on_cooldown(user_id, "duel")
        quest = not db.is_on_cooldown(user_id, "quest")
        working = not db.is_on_cooldown(user_id, "working")
        farm = not db.is_on_cooldown(user_id, "farm")
        horse = not db.is_on_cooldown(user_id, "horse")
        arena = not db.is_on_cooldown(user_id, "arena")
        dungeon = not db.is_on_cooldown(user_id, "dungeon")
        
        # Format the checklist
        def check(is_ready):
            return "✅" if is_ready else "---"

        description = f"""
**🎁 Rewards**
{check(lootbox)} `--` lootbox
{check(card_hand)} `--` card hand
{check(vote)} `--` vote

**🗡️ Experience**
{check(hunt)} `--` hunt
{check(adventure)} `--` adventure
{check(training)} `--` training
{check(duel)} `--` duel
{check(quest)} `--` quest | epic quest

**✨ Progress**
{check(working)} `--` chop | fish | pickup | mine
{check(farm)} `--` farm
{check(horse)} `--` horse breeding | horse race
{check(arena)} `--` arena
{check(dungeon)} `--` dungeon | miniboss
"""

        embed = discord.Embed(
            title=f"{ctx.author.name} — ready",
            description=description.strip(),
            color=0x2b2d31
        )
        embed.set_footer(text='Check the long version of this command with "cd"')

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Ready(bot))