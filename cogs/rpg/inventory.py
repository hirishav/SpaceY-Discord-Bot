import discord
from discord.ext import commands
from database import db

# Define item emojis mapping
EMOJIS = {
    # Items
    "normie fish": "🐟", "golden fish": "🐠", "wooden log": "🪵", "EPIC log": "🌲",
    "apple": "🍎", "banana": "🍌", "potato": "🥔", "carrot": "🥕", "bread": "🍞",
    "flask": "🧪", "wolf skin": "🐺", "zombie eye": "👁️", "unicorn horn": "🦄",
    "dragon essence": "🩸", "wolf fur": "🐺", "bone": "🦴", "dragon scale": "🐉", "fang": "🦷", "gold coin": "🟡",
    
    # Consumables
    "life potion": "🩸", "arena cookie": "🍪", "time cookie": "⏳", "EPIC berry": "🍇",
    "guild ring": "💍", "common lootbox": "📦", "uncommon lootbox": "📦", "rare lootbox": "📦",
    "EPIC lootbox": "📦", "EDGY lootbox": "📦", "OMEGA lootbox": "📦", "GODLY lootbox": "📦",
    "void lootbox": "📦", "wishing token": "🪙", "seed": "🌱", "bread seed": "🌾",
    "ULTRA bait": "🪱", "sleepet potion": "💤", "party popper": "🎉", "mega boost": "🚀",
    "round card": "🃏", "voidernal clock": "⏰", "common card": "🃏",
    
    # Events
    "horse shoe": "🐎", "horseshoe": "🐎",
    "smol coin": "🪙",
    
    # More consumables
    "uncommon card": "🃏", "rare card": "🃏", "EPIC card": "🃏"
}

# Categories
CATEGORIES = {
    "Items": [
        "normie fish", "golden fish", "wooden log", "EPIC log", "apple", "banana",
        "potato", "carrot", "bread", "flask", "wolf skin", "zombie eye", "unicorn horn",
        "dragon essence", "wolf fur", "bone", "dragon scale", "fang", "gold coin"
    ],
    "Consumables": [
        "life potion", "arena cookie", "time cookie", "EPIC berry", "guild ring",
        "common lootbox", "uncommon lootbox", "rare lootbox", "EPIC lootbox",
        "EDGY lootbox", "OMEGA lootbox", "GODLY lootbox", "void lootbox",
        "wishing token", "seed", "bread seed", "ULTRA bait", "sleepet potion",
        "party popper", "mega boost", "round card", "voidernal clock", "common card"
    ],
    "Horse festival event": [
        "horse shoe", "horseshoe"
    ],
    "More consumables": [
        "uncommon card", "rare card", "EPIC card"
    ],
    "Returning event": [
        "smol coin"
    ]
}

class Inventory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['inv', 'i'])
    async def inventory(self, ctx):
        """Tumhara apna inventory bag."""
        user_id = ctx.author.id
        inv = db.get_inventory(user_id)
        
        embed = discord.Embed(
            title=f"{ctx.author.name} — inventory",
            color=0x2b2d31
        )
        
        # Organize items by category
        categorized_items = {cat: [] for cat in CATEGORIES}
        uncategorized_items = []
        
        for item_name, amount in inv.items():
            found = False
            for cat, items_in_cat in CATEGORIES.items():
                if item_name in items_in_cat:
                    emoji = EMOJIS.get(item_name, "🔹")
                    display_name = item_name
                    if display_name == "smol coin" and amount != 1:
                        display_name = "smol coins"
                    categorized_items[cat].append(f"{emoji} **{display_name}**: {amount:,}")
                    found = True
                    break
            if not found:
                emoji = EMOJIS.get(item_name, "🔹")
                uncategorized_items.append(f"{emoji} **{item_name}**: {amount:,}")
                
        # To match screenshot, we add items left to right if they aren't empty
        # Actually Epic RPG uses fields for this. We will add them dynamically.
        # Epic RPG does 3 columns:
        # Items | Consumables | Horse festival event
        # More consumables | Returning event | (empty)
        
        col1 = categorized_items["Items"]
        col2 = categorized_items["Consumables"]
        col3 = categorized_items["Horse festival event"]
        
        if col1 or col2 or col3:
            embed.add_field(name="Items", value="\n".join(col1) if col1 else "None", inline=True)
            embed.add_field(name="Consumables", value="\n".join(col2) if col2 else "None", inline=True)
            if col3:
                embed.add_field(name="Horse festival event", value="\n".join(col3), inline=True)
            else:
                embed.add_field(name="\u200b", value="\u200b", inline=True)

        col4 = categorized_items["More consumables"]
        col5 = categorized_items["Returning event"]
        col6 = uncategorized_items
        
        if col4 or col5 or col6:
            if col4:
                embed.add_field(name="More consumables", value="\n".join(col4), inline=True)
            if col5:
                embed.add_field(name="Returning event", value="\n".join(col5), inline=True)
            if col6:
                embed.add_field(name="Other", value="\n".join(col6), inline=True)
                
        embed.set_footer(text="horse festival event > rpg horse festival")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Inventory(bot))
