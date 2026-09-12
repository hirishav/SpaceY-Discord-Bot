from discord.ext import commands
from discord import app_commands
import discord
import config

def is_owner():
    """
    A custom check that verifies if the invoking user is the bot owner
    specified in the config.
    Can be used for both standard commands and slash commands (app_commands).
    """
    
    # For slash commands (app_commands.check)
    def app_predicate(interaction: discord.Interaction) -> bool:
        if interaction.user.id == config.OWNER_ID:
            return True
        raise app_commands.CheckFailure("Ye command sirf bot owner use kar sakta hai. 😅")
    
    return app_commands.check(app_predicate)

# Alternatively, a decorator for traditional commands, though we prioritize app_commands
def is_owner_ctx():
    async def predicate(ctx: commands.Context) -> bool:
        if ctx.author.id == config.OWNER_ID:
            return True
        raise commands.CheckFailure("Ye command sirf bot owner use kar sakta hai. 😅")
    return commands.check(predicate)
