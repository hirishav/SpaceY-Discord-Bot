import os
import logging
from dotenv import load_dotenv

# Set up standard logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
log = logging.getLogger("SpaceY.Config")

# Load environment variables from .env file
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OWNER_ID_STR = os.getenv("OWNER_ID")

OWNER_ID = None

if not DISCORD_TOKEN:
    log.error("DISCORD_TOKEN is not set in the environment variables.")
    raise ValueError("Missing DISCORD_TOKEN. Please set it in your .env file.")

if not OWNER_ID_STR:
    log.error("OWNER_ID is not set in the environment variables.")
    raise ValueError("Missing OWNER_ID. Please set it in your .env file.")
else:
    try:
        OWNER_ID = int(OWNER_ID_STR)
    except ValueError:
        log.error("OWNER_ID must be a valid integer ID.")
        raise ValueError("Invalid OWNER_ID format. Must be an integer.")

BACKUP_CHANNEL_ID_STR = os.getenv("BACKUP_CHANNEL_ID")
BACKUP_CHANNEL_ID = None

if BACKUP_CHANNEL_ID_STR:
    try:
        BACKUP_CHANNEL_ID = int(BACKUP_CHANNEL_ID_STR)
    except ValueError:
        log.warning("BACKUP_CHANNEL_ID is not a valid integer. Backups will be disabled.")
else:
    log.warning("BACKUP_CHANNEL_ID is not set. Backups will be disabled.")

log.info("Configuration loaded successfully.")
