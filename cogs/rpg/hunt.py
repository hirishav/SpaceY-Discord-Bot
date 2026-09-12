import discord
from discord.ext import commands
import random
from database import db

class Hunt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hunt(self, ctx):
        """Jungle me shikaar karo aur XP kamao."""
        user_id = ctx.author.id
        
        if db.is_on_cooldown(user_id, "hunt"):
            cd_time = db.get_cooldown(user_id, "hunt")
            remaining = db.format_time_remaining(cd_time)
            await ctx.send(f"Abhi hunt par nahi jaa sakte! **{remaining}** wait karo.")
            return
            
        xp_gained = random.randint(1500, 3500)
        coins_gained = random.randint(100, 600)
        
        db.add_xp(user_id, xp_gained)
        db.add_coins(user_id, coins_gained)
        
        db.set_cooldown(user_id, "hunt", 1 * 60) # 1 minute
        
        # Cosmetic HP for now
        hp_lost = random.randint(10, 150)
        max_hp = 364
        hp_remaining = max_hp - hp_lost
        
        mobs = [
            ("🦄", "UNICORN", ["common lootbox", "unicorn horn", "horseshoe", "smol coin"]),
            ("🐺", "WOLF", ["common lootbox", "wolf fur", "bone", "smol coin"]),
            ("🐉", "DRAGON", ["common lootbox", "dragon scale", "gold coin", "smol coin"]),
            ("🦇", "BAT", ["common lootbox", "bat wing", "fang", "smol coin"])
        ]
        
        emoji, mob_name, possible_drops = random.choice(mobs)
        
        msg = f"**{ctx.author.name}** found and killed a {emoji} **{mob_name}**\n"
        msg += f"Earned {coins_gained:,} coins and {xp_gained:,} XP\n"
        msg += f"Lost {hp_lost} HP, remaining HP is {hp_remaining}/{max_hp}\n"
        
        drops = random.sample(possible_drops, k=random.randint(2, len(possible_drops)))
        for drop in drops:
            db.add_item(user_id, drop, 1)
            
            # Formatting drop text
            if drop == "common lootbox":
                drop_emoji = "📦"
            elif "horn" in drop:
                drop_emoji = "🦄"
            elif drop == "horseshoe":
                drop_emoji = "🐎"
            elif drop == "smol coin":
                drop_emoji = "🪙"
            elif drop == "wolf fur":
                drop_emoji = "🐺"
            elif drop == "bone":
                drop_emoji = "🦴"
            elif drop == "dragon scale":
                drop_emoji = "🐉"
            elif drop == "gold coin":
                drop_emoji = "🟡"
            elif drop == "bat wing":
                drop_emoji = "🦇"
            elif drop == "fang":
                drop_emoji = "🦷"
            else:
                drop_emoji = "🔹"
                
            msg += f"**{ctx.author.name}** got 1 {drop_emoji} {drop}\n"

        await ctx.send(msg)

async def setup(bot):
    await bot.add_cog(Hunt(bot))
