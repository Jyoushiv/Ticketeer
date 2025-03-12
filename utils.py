
import discord
import random
import logging

logger = logging.getLogger(__name__)

def get_embed_color():
    """
    Generate a random color for embeds.

    Returns:
        discord.Color: A random color object
    """
    return discord.Color.from_rgb(
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )

async def log_ticket_event(guild, event_type, user, channel=None, closed_by=None):
    """
    Log a ticket event to the ticket-logs channel

    Args:
        guild: The Discord guild
        event_type: Type of event (created, closed)
        user: The user who created the ticket
        channel: The ticket channel (optional)
        closed_by: The user who closed the ticket (optional)
    """
    logs_channel = discord.utils.get(guild.text_channels, name="ticket-logs")
    if not logs_channel:
        logger.warning(f"Ticket logs channel not found in guild {guild.name}")
        return

    if event_type == "created":
        embed = discord.Embed(
            title="Ticket Created",
            description=f"Ticket created by {user.mention}",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )
        if channel:
            embed.add_field(name="Channel", value=channel.mention)
    
    elif event_type == "closed":
        embed = discord.Embed(
            title="Ticket Closed",
            description=f"Ticket for {user.mention} was closed",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )
        if closed_by:
            embed.add_field(name="Closed By", value=closed_by.mention)

    else:
        embed = discord.Embed(
            title="Ticket Event",
            description=f"Ticket event for {user.mention}",
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow()
        )

    await logs_channel.send(embed=embed)
    logger.info(f"Logged ticket {event_type} event for user {user}")
