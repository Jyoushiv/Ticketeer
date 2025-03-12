import discord
from discord.ext import commands
import logging
import os
from commands import setup_commands

logger = logging.getLogger(__name__)

def setup_bot():
    """
    Set up the Discord bot with intents and command prefix.
    Returns the configured bot instance.
    """
    # Set up intents for the bot
    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True  # Required for reading message content
    intents.guilds = True
    
    # Get the command prefix from environment variables or use default
    command_prefix = os.environ.get("COMMAND_PREFIX", "!")
    
    # Create the bot instance
    bot = commands.Bot(command_prefix=command_prefix, intents=intents, help_command=None)
    
    # Event: Bot is ready
    @bot.event
    async def on_ready():
        """Event triggered when the bot is ready and connected to Discord."""
        logger.info(f"{bot.user.name} has connected to Discord!")
        logger.info(f"Bot is in {len(bot.guilds)} guild(s)")
        
        # Set bot status
        await bot.change_presence(activity=discord.Game(f"Type {command_prefix}help for commands"))
    
    # Event: Handle errors in commands
    @bot.event
    async def on_command_error(ctx, error):
        """Global error handler for command errors."""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"Command not found. Try `{command_prefix}help` to see available commands.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument: {error.param.name}")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"Bad argument provided: {error}")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
        else:
            logger.error(f"Command error: {error}")
            await ctx.send(f"An error occurred: {error}")
    
    # Event: Handle messages
    @bot.event
    async def on_message(message):
        """Event triggered when a message is sent in a channel the bot can see."""
        # Don't respond to our own messages
        if message.author == bot.user:
            return
        
        # Process commands
        await bot.process_commands(message)
    
    # Setup all the commands
    setup_commands(bot)
    
    return bot
