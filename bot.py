import discord
from discord.ext import commands
import logging
import os
import config

log = logging.getLogger("SpaceY.Bot")

class SpaceYBot(commands.Bot):
    def __init__(self):
        # Intents setup: Only what is required right now.
        intents = discord.Intents.default()
        # Enable message intents for prefix commands
        intents.message_content = True
        
        super().__init__(
            command_prefix=commands.when_mentioned_or('s ', 'S ', 's', 'S'),
            intents=intents,
            case_insensitive=True,
            help_command=None # We'll build custom help via slash commands later
        )

    async def setup_hook(self):
        """
        Executed exactly once when the bot starts.
        Used to load cogs/extensions and sync tree commands.
        """
        log.info("Setting up extensions...")
        
        # Load Cogs automatically from the cogs directory
        cogs_dir = "cogs"
        if not os.path.exists(cogs_dir):
            os.makedirs(cogs_dir)

        # Example structure: cogs/owner/owner_set_status.py
        for root, dirs, files in os.walk(cogs_dir):
            for file in files:
                if file.endswith('.py') and not file.startswith('__'):
                    # e.g., 'cogs/owner/owner_set_status.py' -> 'cogs.owner.owner_set_status'
                    # replace backslashes (Windows) or slashes (Linux) with dots
                    rel_path = os.path.relpath(os.path.join(root, file), start=".")
                    cog_path = rel_path.replace(os.sep, '.')[:-3]
                    try:
                        await self.load_extension(cog_path)
                        log.info(f"Loaded extension: {cog_path}")
                    except Exception as e:
                        log.error(f"Failed to load extension {cog_path}: {e}")
        
        # Syncing commands globally. Note: Global sync can take up to an hour to propagate on Discord.
        log.info("Syncing slash commands...")
        try:
            synced = await self.tree.sync()
            log.info(f"Successfully synced {len(synced)} command(s).")
        except Exception as e:
            log.error(f"Failed to sync commands: {e}")

    async def on_ready(self):
        """
        Executed when the bot successfully connects to Discord.
        """
        log.info(f"Logged in as {self.user} (ID: {self.user.id})")
        log.info("Space Y is ready for launch!")

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        # Check if the message is exactly just mentioning the bot
        if message.content in [f"<@{self.user.id}>", f"<@!{self.user.id}>"]:
            embed = discord.Embed(
                description=f"Hello **{message.author.name}**! 👋\nIs server me mera current prefix `s` hai.\nAap commands ko `s help` tarike se use kar sakte hain!",
                color=0x2b2d31
            )
            await message.channel.send(embed=embed)

        # Ensure commands still process
        await self.process_commands(message)

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """
        Basic error handling for traditional commands.
        """
        if isinstance(error, commands.CommandNotFound):
            if ctx.invoked_with:
                import difflib
                commands_list = [c.name for c in self.commands if not c.hidden]
                matches = difflib.get_close_matches(ctx.invoked_with, commands_list, n=1, cutoff=0.5)
                if matches:
                    await ctx.send(f"Command not found. Did you mean `{ctx.prefix}{matches[0]}`?")
            return
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(str(error))
        else:
            log.error(f"Ignoring exception in command {ctx.command}: {error}")
            await ctx.send("Oops! Kuch technical issue aa gaya. Developer ko check karna padega.")

bot = SpaceYBot()

# Global App Command error handler
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    if isinstance(error, discord.app_commands.CheckFailure):
        await interaction.response.send_message(str(error), ephemeral=True)
    else:
        log.error(f"AppCommand error: {error}")
        try:
            msg = "Oops! Kuch technical issue aa gaya. Developer ko check karna padega."
            if interaction.response.is_done():
                await interaction.followup.send(msg, ephemeral=True)
            else:
                await interaction.response.send_message(msg, ephemeral=True)
        except discord.HTTPException:
            pass

if __name__ == "__main__":
    bot.run(config.DISCORD_TOKEN)
