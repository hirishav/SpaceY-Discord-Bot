import discord
from discord.ext import commands
from discord import app_commands
import logging
from typing import Literal

from utils.checks import is_owner

log = logging.getLogger("SpaceY.OwnerStatus")

class OwnerStatus(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _update_status(self, interaction: discord.Interaction, status_type: str, activity_type: str, text: str, stream_url: str):
        # 1. Parse Status
        status_map = {
            "online": discord.Status.online,
            "idle": discord.Status.idle,
            "dnd": discord.Status.dnd,
            "invisible": discord.Status.invisible
        }
        discord_status = status_map[status_type]

        # 2. Parse Activity
        if activity_type == "custom":
            activity = discord.CustomActivity(name=text)
        else:
            activity_map = {
                "playing": discord.ActivityType.playing,
                "watching": discord.ActivityType.watching,
                "listening": discord.ActivityType.listening,
                "streaming": discord.ActivityType.streaming
            }
            discord_activity_type = activity_map[activity_type]
            url = stream_url if activity_type == "streaming" else None
            activity = discord.Activity(type=discord_activity_type, name=text, url=url)

        # 3. Update Presence
        try:
            await self.bot.change_presence(status=discord_status, activity=activity)
            
            # 4. Respond in Hinglish
            await interaction.response.send_message(
                f"Status successfully update ho gaya! 👀\nBot abhi `{activity_type.capitalize()} {text}` status par hai.",
                ephemeral=True
            )
            log.info(f"Owner updated presence: Status={status_type}, Activity={activity_type}, Text='{text}'")
            
        except Exception as e:
            log.error(f"Failed to change presence: {e}")
            await interaction.response.send_message("Technical issue aa gaya status change karne me. 😅", ephemeral=True)

    @app_commands.command(
        name="owner_set_status",
        description="Bot ka status aur activity change karo. (Sirf Owner ke liye)"
    )
    @is_owner()
    @app_commands.describe(
        status_type="Online, Idle, DND, ya Invisible",
        activity_type="Playing, Watching, Listening, Streaming, ya Custom",
        text="Status me kya text dikhana hai?",
        stream_url="Streaming ke liye Twitch ya YouTube link (Discord sirf inhi pe button dikhata hai)"
    )
    async def set_status(
        self,
        interaction: discord.Interaction,
        status_type: Literal["online", "idle", "dnd", "invisible"],
        activity_type: Literal["playing", "watching", "listening", "streaming", "custom"],
        text: str,
        stream_url: str = "https://twitch.tv/discord"
    ):
        await self._update_status(interaction, status_type, activity_type, text, stream_url)

    @app_commands.command(
        name="ss",
        description="Bot ka status aur activity change karo. (owner_set_status ka shortcut)"
    )
    @is_owner()
    @app_commands.describe(
        status_type="Online, Idle, DND, ya Invisible",
        activity_type="Playing, Watching, Listening, Streaming, ya Custom",
        text="Status me kya text dikhana hai?",
        stream_url="Streaming ke liye Twitch ya YouTube link"
    )
    async def set_status_alias(
        self,
        interaction: discord.Interaction,
        status_type: Literal["online", "idle", "dnd", "invisible"],
        activity_type: Literal["playing", "watching", "listening", "streaming", "custom"],
        text: str,
        stream_url: str = "https://twitch.tv/discord"
    ):
        await self._update_status(interaction, status_type, activity_type, text, stream_url)

async def setup(bot: commands.Bot):
    await bot.add_cog(OwnerStatus(bot))
