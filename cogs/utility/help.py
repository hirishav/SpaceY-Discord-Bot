import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["h"])
    async def custom_help(self, ctx):
        """Sare commands ki list aur information dekho."""
        embed = discord.Embed(
            title="Space Y RPG - Help Menu",
            description="Yahan saare commands ki jankari hai, aaram se khelo! 🚀\nDefault prefix: `s ` ya `S `",
            color=discord.Color.blurple()
        )
        
        rpg_commands = (
            "`s ready` (ya `s rd`) - Check karo kaunse commands ready hain.\n"
            "`s cooldowns` (ya `s cd`) - Commands ka cooldown timer dekho.\n"
            "`s daily` - Roz ka inam (coins aur potions) claim karo.\n"
            "`s weekly` - Hafte ka bada inam claim karo.\n"
            "`s farm` - Kheti karo aur XP / items kamao.\n"
            "`s shop` - Bazaar se items kharido.\n"
            "`s horse` - Apne ghode ka status dekho.\n"
            "`s dungeon` - Dungeon me ghuso (key chahiye).\n"
            "`s arena` - PvP arena me lado."
        )
        embed.add_field(name="🗡️ RPG Commands", value=rpg_commands, inline=False)
        
        owner_commands = (
            "`/owner_set_status` (Slash Command) - Bot ka status change karne ke liye (Sirf owner)."
        )
        embed.add_field(name="👑 Owner Commands", value=owner_commands, inline=False)
        
        embed.set_footer(text="Space Y | RPG Adventure")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
