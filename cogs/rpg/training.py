import discord
from discord.ext import commands
import random
from database import db

class TrainingView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=15.0)
        self.user_id = user_id
        self.answered = False

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Yeh tumhara training nahi hai!", ephemeral=True)
            return False
        return True
        
    async def on_timeout(self):
        if not self.answered and hasattr(self, 'message'):
            for child in self.children:
                child.disabled = True
            try:
                await self.message.edit(view=self)
            except:
                pass

    @discord.ui.button(label="yes", style=discord.ButtonStyle.success)
    async def btn_yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.answered = True
        for child in self.children:
            child.disabled = True
            
        xp_gained = random.randint(10000, 15000)
        db.add_xp(self.user_id, xp_gained)
        
        await interaction.response.edit_message(view=self)
        await interaction.channel.send(f"Well done, **{interaction.user.name}**!\nEarned {xp_gained:,} XP")

    @discord.ui.button(label="no", style=discord.ButtonStyle.danger)
    async def btn_no(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.answered = True
        for child in self.children:
            child.disabled = True
            
        await interaction.response.edit_message(view=self)
        await interaction.channel.send(f"**{interaction.user.name}**, that was incorrect!")

class Training(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['tr'])
    async def training(self, ctx):
        """Apne skills ko train karo."""
        user_id = ctx.author.id
        
        if db.is_on_cooldown(user_id, "training"):
            cd_time = db.get_cooldown(user_id, "training")
            remaining = db.format_time_remaining(cd_time)
            await ctx.send(f"Training ke baad thakan hoti hai! **{remaining}** aaram karo.")
            return
            
        db.set_cooldown(user_id, "training", 15 * 60) # 15 minutes
        
        msg = f"**{ctx.author.name}** is training in the mine!\n"
        msg += "Do you have more than 5 💎 rubies in your inventory?\n"
        msg += "Answer with `yes` or `no`! You have 15 seconds!"
        
        view = TrainingView(user_id)
        message = await ctx.send(msg, view=view)
        view.message = message

async def setup(bot):
    await bot.add_cog(Training(bot))
