import discord
from discord.ext import commands
from database import db

class Bank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['dep'])
    async def deposit(self, ctx, amount: str):
        """Bank mein coins jama karo"""
        user_id = ctx.author.id
        user_coins = db.get_coins(user_id)
        
        if user_coins <= 0:
            await ctx.send("Tumhare paas deposit karne ke liye coins hi nahi hain! 😅")
            return
            
        if amount.lower() == 'all':
            dep_amount = user_coins
        else:
            try:
                dep_amount = int(amount)
            except ValueError:
                await ctx.send("Sahi amount daalo bhai, ya 'all' likho.")
                return
                
        if dep_amount <= 0:
            await ctx.send("Amount 0 se bada hona chahiye.")
            return
            
        if dep_amount > user_coins:
            await ctx.send(f"Bhai tumhare paas sirf **{user_coins:,}** coins hain. Itna zyada kaise doge?")
            return
            
        # Deduct coins and add to bank
        db.add_coins(user_id, -dep_amount)
        db.update_bank(user_id, dep_amount)
        
        embed = discord.Embed(
            title="🏦 Bank Deposit",
            description=f"✅ **{dep_amount:,}** coins successfully bank mein deposit kar diye gaye!\n\n> Naya Balance:\n> 🪙 **Coins:** {db.get_coins(user_id):,}\n> 🏦 **Bank:** {db.get_user_all(user_id)['bank']:,}",
            color=discord.Color.brand_green()
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['with'])
    async def withdraw(self, ctx, amount: str):
        """Bank se coins nikaalo"""
        user_id = ctx.author.id
        user_data = db.get_user_all(user_id)
        user_bank = user_data['bank'] if user_data else 0
        
        if user_bank <= 0:
            await ctx.send("Tumhara bank account khaali hai bhai! 😭")
            return
            
        if amount.lower() == 'all':
            with_amount = user_bank
        else:
            try:
                with_amount = int(amount)
            except ValueError:
                await ctx.send("Sahi amount daalo bhai, ya 'all' likho.")
                return
                
        if with_amount <= 0:
            await ctx.send("Amount 0 se bada hona chahiye.")
            return
            
        if with_amount > user_bank:
            await ctx.send(f"Bank mein sirf **{user_bank:,}** coins hain.")
            return
            
        # Deduct from bank and add to coins
        db.update_bank(user_id, -with_amount)
        db.add_coins(user_id, with_amount)
        
        embed = discord.Embed(
            title="🏦 Bank Withdraw",
            description=f"✅ **{with_amount:,}** coins bank se nikaal liye gaye!\n\n> Naya Balance:\n> 🪙 **Coins:** {db.get_coins(user_id):,}\n> 🏦 **Bank:** {db.get_user_all(user_id)['bank']:,}",
            color=discord.Color.dark_theme()
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Bank(bot))
