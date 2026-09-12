# Space Y Discord RPG Bot

Space Y is a modern Discord RPG bot written in Python using `discord.py` and `python-dotenv`.
Currently, this project represents the solid foundation upon which future RPG systems (hunt, adventure, economy, dungeons, etc.) will be built.

## Project Structure
- `bot.py`: Main entry point and bot core class.
- `config.py`: Configuration and environment loading.
- `cogs/`: Contains all bot commands, organized by category (e.g., `cogs/owner`, `cogs/rpg`). Each command is typically its own file.
- `utils/`: Reusable utilities and checks.

## Setup Instructions

1. **Install Dependencies**
   Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configuration**
   Copy the `.env.example` file to `.env` (or rename it manually):
   Open the `.env` file and populate it with:
   - `DISCORD_TOKEN`: Your actual Discord bot token.
   - `OWNER_ID`: Your personal Discord user ID (for owner-only commands).

3. **Run the Bot**
   Start the bot by running:
   ```bash
   python bot.py
   ```

## Owner Commands
- `/owner_set_status`: A slash command to change the bot's presence (Status and Activity).
