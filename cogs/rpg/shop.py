import discord
from discord.ext import commands

SHOP_ITEMS = [
    {"name": "life potion", "emoji": "🩸", "price": 25, "desc": "Health badhane ke liye."},
    {"name": "basic armor", "emoji": "🟫", "price": 200, "desc": "[+2 def] Lakdi ka sasta armor."},
    {"name": "basic sword", "emoji": "🗡️", "price": 150, "desc": "[+1 atk] Kuch na hone se behtar hai."},
    {"name": "basic horse", "emoji": "🐎", "price": 500, "desc": "[tier I] Ek normal ghoda."},
    {"name": "dungeon key", "emoji": "🗝️", "price": 600000, "desc": "Dungeon me entry ke liye zaroori."},
    {"name": "lottery ticket", "emoji": "🎫", "price": 10000, "desc": "Lottery me kismat aazmao."},
    {"name": "seed", "emoji": "🌱", "price": 4000, "desc": "Kheti (farm) karne ke kaam aata hai."},
    {"name": "common lootbox", "emoji": "📦", "price": 800, "desc": "Kuch saste items nikal sakte hain."},
    {"name": "uncommon lootbox", "emoji": "📦", "price": 6000, "desc": "Thode behtar items ke liye."},
    {"name": "rare lootbox", "emoji": "📦", "price": 40000, "desc": "Bahut saare items mil sakte hain."},
    {"name": "EPIC lootbox", "emoji": "📦", "price": 150000, "desc": "Kamaal ke items milne ka chance!"},
    {"name": "life boost A", "emoji": "✨", "price": 10000, "desc": "+10 temporary max health."}
]

class ShopPagination(discord.ui.View):
    def __init__(self, author_id, pages):
        super().__init__(timeout=60.0)
        self.author_id = author_id
        self.pages = pages
        self.current_page = 0
        self.update_buttons()

    def update_buttons(self):
        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page == len(self.pages) - 1

    @discord.ui.button(label="◀️", style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Ye tumhara shop menu nahi hai!", ephemeral=True)
            return
            
        self.current_page -= 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)

    @discord.ui.button(label="▶️", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Ye tumhara shop menu nahi hai!", ephemeral=True)
            return
            
        self.current_page += 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def shop(self, ctx):
        """Bazaar dekho aur items kharido!"""
        
        items_per_page = 7
        pages = []
        
        for i in range(0, len(SHOP_ITEMS), items_per_page):
            chunk = SHOP_ITEMS[i:i + items_per_page]
            
            description = f"**Bazaar NPC:** Hey, {ctx.author.name}! Kuch bhi kharidna ho to `s buy [item]` likho.\n\n"
            
            for item in chunk:
                description += f"{item['emoji']} **{item['name']}** | {item['price']:,} 🟡\n{item['desc']}\n\n"
            
            page_num = (i // items_per_page) + 1
            total_pages = (len(SHOP_ITEMS) + items_per_page - 1) // items_per_page
            
            embed = discord.Embed(
                title=f"Shop - Page {page_num}/{total_pages}",
                description=description,
                color=discord.Color.dark_theme()
            )
            pages.append(embed)

        view = ShopPagination(ctx.author.id, pages)
        await ctx.send(embed=pages[0], view=view)

    @commands.command()
    async def buy(self, ctx, *, item_and_amount: str = None):
        """Koi item kharido."""
        if not item_and_amount:
            await ctx.send("Bhai, kya kharidna hai? Naam toh batao! (e.g. `s buy life potion`)")
            return
            
        parts = item_and_amount.split()
        amount = 1
        item_name = item_and_amount.lower()
        
        if len(parts) > 1 and parts[-1].isdigit():
            amount = int(parts[-1])
            if amount <= 0:
                await ctx.send("Valid amount daalo bhai!")
                return
            item_name = " ".join(parts[:-1]).lower()
            
        # Check if item exists in shop
        item_data = None
        for item in SHOP_ITEMS:
            if item["name"].lower() == item_name:
                item_data = item
                break
                
        if not item_data:
            await ctx.send("Ye item bazaar me nahi milta! `s shop` check karo.")
            return
            
        user_id = ctx.author.id
        total_price = item_data["price"] * amount
        
        # Check if user has enough coins
        from database import db
        current_coins = db.get_coins(user_id)
        if current_coins < total_price:
            await ctx.send(f"Tumhare paas itne coins nahi hain! {total_price - current_coins:,} 🟡 aur chahiye.")
            return
            
        # Deduct coins and give item
        db.add_coins(user_id, -total_price)
        db.add_item(user_id, item_data["name"], amount)
        
        embed = discord.Embed(
            title=f"{ctx.author.name} — purchase successful",
            description=f"Tumne **{amount} {item_data['name']}** kharid liya!\n\n**-{total_price:,}** 🟡 coins",
            color=0x2b2d31
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Shop(bot))