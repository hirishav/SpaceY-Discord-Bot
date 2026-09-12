import discord
from discord.ext import commands
import random
from database import db

class OpenBox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def open(self, ctx, *, box_type: str):
        """Lootboxes open karo"""
        user_id = ctx.author.id
        
        # Format box type if user didn't write "lootbox"
        box_name = box_type.lower().strip()
        if not box_name.endswith("lootbox"):
            box_name += " lootbox"
            
        amount = db.get_item_amount(user_id, box_name)
        if amount <= 0:
            await ctx.send(f"**{ctx.author.name}**, tumhare paas koi `{box_name}` nahi hai!")
            return
            
        # Deduct the box
        db.add_item(user_id, box_name, -1)
        
        # Decide rewards based on box type
        coins_reward = 0
        xp_reward = 0
        items_reward = []
        
        if box_name == "common lootbox":
            coins_reward = random.randint(500, 2000)
            xp_reward = random.randint(500, 2000)
            items_reward.append(("life potion", random.randint(1, 2)))
        elif box_name == "rare lootbox":
            coins_reward = random.randint(2000, 5000)
            xp_reward = random.randint(2000, 5000)
            items_reward.append(("life potion", random.randint(2, 5)))
            items_reward.append(("epic coin", random.randint(1, 3)))
        elif box_name == "epic lootbox":
            coins_reward = random.randint(5000, 15000)
            xp_reward = random.randint(5000, 15000)
            items_reward.append(("life potion", random.randint(5, 10)))
            items_reward.append(("epic coin", random.randint(5, 15)))
        else:
            # Fallback for unknown boxes
            coins_reward = random.randint(100, 500)
            xp_reward = random.randint(100, 500)
            
        # Give rewards
        if coins_reward > 0:
            db.add_coins(user_id, coins_reward)
        if xp_reward > 0:
            db.add_xp(user_id, xp_reward)
            
        rewards_text = f"🪙 **{coins_reward:,}** coins\n⭐ **{xp_reward:,}** XP\n"
        for item, qty in items_reward:
            db.add_item(user_id, item, qty)
            rewards_text += f"🎁 **{qty}x** {item}\n"
            
        embed = discord.Embed(
            title=f"📦 Opened {box_name.title()}",
            description=f"**{ctx.author.name}**, you opened a {box_name} and got:\n\n{rewards_text}",
            color=discord.Color.gold()
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(OpenBox(bot))
