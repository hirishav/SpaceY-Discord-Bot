import discord
from discord.ext import commands
from database import db

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['p', 'pr'])
    async def profile(self, ctx):
        user_id = ctx.author.id
        user_data = db.get_user_all(user_id)
        
        if not user_data:
            db.add_coins(user_id, 0)
            user_data = db.get_user_all(user_id)
            
        xp = user_data['xp']
        level = (xp // 5000) + 1
        xp_next = level * 5000
        percent = (xp / xp_next) * 100
        
        global_rank = db.get_global_rank(user_id)
        
        # Base setup
        embed = discord.Embed(color=0x2b2d31) # A sleek dark gray/Discord dark theme color
        embed.set_author(name=f"{ctx.author.name}'s Profile", icon_url=ctx.author.display_avatar.url)
        
        # Time travel badges
        description = ""
        if user_data['time_travels'] > 0:
            description = f"🌟 **Eggspert Time Traveler** (TT: {user_data['time_travels']})\n"
        description += f"🏆 **Global Rank:** #{global_rank}\n\n"
        embed.description = description
        
        progress = (
            f"> **Level:** `{level}` ({percent:.1f}%)\n"
            f"> **XP:** `{xp:,}` / `{xp_next:,}`\n"
            f"> **Area:** `{user_data['area']}`\n"
        )
        
        stats = (
            f"> 🗡️ **ATK:** `{user_data['attack']}`\n"
            f"> 🛡️ **DEF:** `{user_data['defense']}`\n"
            f"> ❤️ **HP:** `{user_data['hp']} / {user_data['max_hp']}`\n"
        )
        
        # Horse Tier logic (festive = 🐎)
        horse_tier = user_data['horse_tier']
        horse_str = f"🐎 Tier {horse_tier}" if horse_tier > 0 else "None"
        
        equipment = (
            f"> 🗡️ **Sword:** `Ultimate`\n"
            f"> 🛡️ **Armor:** `Perfect`\n"
            f"> 🐎 **Horse:** `{horse_str}`\n"
        )
        
        money = (
            f"> 🪙 **Coins:** `{user_data['coins']:,}`\n"
            f"> 💠 **EPIC Coins:** `{user_data['epic_coins']:,}`\n"
            f"> 🏦 **Bank:** `{user_data['bank']:,}`\n"
        )
        
        # Adding fields creatively
        embed.add_field(name="📈 Progress", value=progress, inline=True)
        embed.add_field(name="⚔️ Combat Stats", value=stats, inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=False) # Spacer
        
        embed.add_field(name="🛡️ Equipment", value=equipment, inline=True)
        embed.add_field(name="💰 Wealth", value=money, inline=True)
        
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.set_footer(text="SpaceY RPG • Global Leaderboard synced")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Profile(bot))
