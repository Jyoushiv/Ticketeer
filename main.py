
import os
import logging
from keep_alive import keep_alive
from bot import setup_bot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """
    Main entry point for the Discord bot.
    Sets up the keep-alive server and starts the bot.
    """
    logger.info("Starting Discord Bot...")
    
    # Start the keep-alive web server to prevent Replit from sleeping
    keep_alive()
    
    # Get the token from environment variables
    token = os.environ.get("DISCORD_TOKEN")
    
    if not token:
        logger.error("No Discord token found. Please set the DISCORD_TOKEN environment variable.")
        return
    
    try:
        # Setup and run the bot
        bot = setup_bot()
        logger.info("Connecting to Discord...")
        bot.run(token)
    except Exception as e:
        logger.error(f"Error running the bot: {e}")

if __name__ == "__main__":
    main()
