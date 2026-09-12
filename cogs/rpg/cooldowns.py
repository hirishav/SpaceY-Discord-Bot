import discord
from discord.ext import commands
import time
from database import db

class Cooldowns(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['cd'])
    async def cooldowns(self, ctx):
        """Dikhaata hai kaun se commands cooldown par hain."""
        user_id = ctx.author.id
        
        # Get cooldowns
        lootbox = db.get_cooldown(user_id, "lootbox")
        card_hand = db.get_cooldown(user_id, "card_hand")
        vote = db.get_cooldown(user_id, "vote")
        hunt = db.get_cooldown(user_id, "hunt")
        adventure = db.get_cooldown(user_id, "adventure")
        training = db.get_cooldown(user_id, "training")
        duel = db.get_cooldown(user_id, "duel")
        quest = db.get_cooldown(user_id, "quest")
        working = db.get_cooldown(user_id, "working")
        farm = db.get_cooldown(user_id, "farm")
        horse = db.get_cooldown(user_id, "horse")
        arena = db.get_cooldown(user_id, "arena")
        dungeon = db.get_cooldown(user_id, "dungeon")
        
        # Format the checklist
        def check(cd_time):
            if cd_time > time.time():
                return f"🕓 **{db.format_time_remaining(cd_time)}**"
            return "✅"

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
            title=f"{ctx.author.name} — cooldowns",
            description=description.strip(),
            color=0x2b2d31
        )
        embed.set_footer(text='Check the short version of this command with "rd"')

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Cooldowns(bot))