import discord
from discord.ext import commands, tasks
import logging
import os
import config
import time

log = logging.getLogger("SpaceY.Backup")

class Backup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if config.BACKUP_CHANNEL_ID:
            self.backup_loop.start()
        else:
            log.warning("BACKUP_CHANNEL_ID not set, backup loop will not start.")

    def cog_unload(self):
        self.backup_loop.cancel()

    @tasks.loop(minutes=30)
    async def backup_loop(self):
        """Send the SQLite database file to the backup channel every 30 minutes."""
        await self.bot.wait_until_ready()
        
        channel = self.bot.get_channel(config.BACKUP_CHANNEL_ID)
        if not channel:
            try:
                channel = await self.bot.fetch_channel(config.BACKUP_CHANNEL_ID)
            except discord.NotFound:
                log.error(f"Backup channel {config.BACKUP_CHANNEL_ID} not found. Ensure bot is in the server.")
                return
            except discord.Forbidden:
                log.error(f"Bot lacks permissions to access backup channel {config.BACKUP_CHANNEL_ID}.")
                return
            except Exception as e:
                log.error(f"Error fetching backup channel: {e}")
                return

        db_path = os.path.join(os.path.dirname(__file__), "..", "..", "database", "spacey.db")
        
        if not os.path.exists(db_path):
            log.warning(f"Database file not found at {db_path}. Skipping backup.")
            return

        try:
            time_str = time.strftime("%A, %d %B, %Y %I:%M %p")
            file = discord.File(db_path, filename="spacey.db")
            
            await channel.send(
                content=f"Database Backup at {time_str}",
                file=file
            )
            log.info("Database backup successfully uploaded to Discord.")
        except Exception as e:
            log.error(f"Failed to upload database backup: {e}")

async def setup(bot):
    await bot.add_cog(Backup(bot))
