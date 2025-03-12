import discord
from discord.ext import commands
import logging
import random
import os
from utils import get_embed_color
from discord.ui import Button, View

logger = logging.getLogger(__name__)

def setup_commands(bot):
    """
    Set up all commands for the Discord bot.
    
    Args:
        bot: The Discord bot instance
    """
    
    @bot.command(name="help")
    async def help_command(ctx):
        """Display help information for available commands."""
        prefix = bot.command_prefix
        embed = discord.Embed(
            title="Bot Help",
            description=f"Here are the commands you can use with this bot (prefix: `{prefix}`)",
            color=get_embed_color()
        )
        
        commands_list = [
            {"name": "help", "description": "Shows this help message"},
            {"name": "ping", "description": "Checks the bot's response time"},
            {"name": "hello", "description": "Greets you with a friendly message"},
            {"name": "roll", "description": "Rolls a dice (e.g., `{prefix}roll 2d6`)"},
            {"name": "info", "description": "Displays information about the bot"},
            {"name": "serverinfo", "description": "Displays information about the server"},
            {"name": "setup_tickets", "description": "Sets up the ticket system with logs (Admin only)"},
            {"name": "close", "description": "Closes the current ticket (use in ticket channels)"},
        ]
        
        for cmd in commands_list:
            embed.add_field(
                name=f"{prefix}{cmd['name']}",
                value=cmd['description'],
                inline=False
            )
            
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        
        await ctx.send(embed=embed)
        logger.info(f"Help command used by {ctx.author}")

    @bot.command(name="ping")
    async def ping_command(ctx):
        """Check the bot's response time."""
        latency = round(bot.latency * 1000)
        await ctx.send(f"Pong! 🏓 Response time: {latency}ms")
        logger.info(f"Ping command used by {ctx.author}")

    @bot.command(name="hello")
    async def hello_command(ctx):
        """Greet the user with a friendly message."""
        greetings = [
            f"Hello, {ctx.author.mention}! How are you doing today?",
            f"Hey there, {ctx.author.mention}! Nice to see you!",
            f"Greetings, {ctx.author.mention}! Hope you're having a great day!",
            f"Hi, {ctx.author.mention}! What can I help you with today?"
        ]
        await ctx.send(random.choice(greetings))
        logger.info(f"Hello command used by {ctx.author}")

    @bot.command(name="roll")
    async def roll_command(ctx, dice: str = "1d6"):
        """
        Roll dice in NdN format.
        
        Args:
            dice: Dice in NdN format (default: 1d6)
        """
        try:
            rolls, limit = map(int, dice.split('d'))
            
            if rolls > 100:
                await ctx.send("I can't roll that many dice!")
                return
                
            if limit > 1000:
                await ctx.send("Dice sides too large!")
                return
                
            results = [random.randint(1, limit) for _ in range(rolls)]
            total = sum(results)
            
            if len(results) == 1:
                await ctx.send(f"🎲 You rolled a {total}")
            else:
                await ctx.send(f"🎲 You rolled {dice} and got: {', '.join(map(str, results))} (Total: {total})")
        except Exception as e:
            await ctx.send(f"Format has to be in NdN (e.g., 2d6). Error: {e}")
        
        logger.info(f"Roll command used by {ctx.author} with argument: {dice}")

    @bot.command(name="info")
    async def info_command(ctx):
        """Display information about the bot."""
        embed = discord.Embed(
            title="Bot Information",
            description="A Discord bot built with discord.py and hosted on Replit",
            color=get_embed_color()
        )
        
        embed.add_field(name="Library", value="discord.py", inline=True)
        embed.add_field(name="Host", value="Replit", inline=True)
        embed.add_field(name="Prefix", value=bot.command_prefix, inline=True)
        embed.add_field(name="Creator", value="A helpful developer", inline=True)
        embed.add_field(name="Servers", value=str(len(bot.guilds)), inline=True)
        embed.add_field(name="Commands", value="Use `!help` to see commands", inline=True)
        
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        
        await ctx.send(embed=embed)
        logger.info(f"Info command used by {ctx.author}")

    @bot.command(name="serverinfo")
    async def serverinfo_command(ctx):
        """Display information about the server."""
        guild = ctx.guild
        
        if not guild:
            await ctx.send("This command can only be used in a server.")
            return
            
        embed = discord.Embed(
            title=f"{guild.name} Information",
            description=f"Server ID: {guild.id}",
            color=get_embed_color()
        )
        
        # Add server information
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
            
        embed.add_field(name="Owner", value=guild.owner.mention if guild.owner else "Unknown", inline=True)
        embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Member Count", value=str(guild.member_count), inline=True)
        embed.add_field(name="Channel Count", value=str(len(guild.channels)), inline=True)
        embed.add_field(name="Role Count", value=str(len(guild.roles)), inline=True)
        embed.add_field(name="Emoji Count", value=str(len(guild.emojis)), inline=True)
        
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        
        await ctx.send(embed=embed)
        logger.info(f"Serverinfo command used by {ctx.author}")
        
    @bot.command(name="setup_tickets")
    @commands.has_permissions(administrator=True)
    async def setup_tickets_command(ctx, staff_role: discord.Role = None):
        """
        Set up ticket system with ticket channel and logs channel.
        
        Args:
            staff_role: The role that can see tickets (optional)
        """
        guild = ctx.guild
        
        if not guild:
            await ctx.send("This command can only be used in a server.")
            return
            
        # Create logs channel if it doesn't exist
        logs_channel = discord.utils.get(guild.text_channels, name="ticket-logs")
        if not logs_channel:
            # Set permissions for logs channel (only admins and staff can see)
            logs_overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
            }
            
            # Add staff role if provided
            if staff_role:
                logs_overwrites[staff_role] = discord.PermissionOverwrite(view_channel=True)
                
                # Store staff role ID in environment variable
                os.environ["STAFF_ROLE_ID"] = str(staff_role.id)
                
            logs_channel = await guild.create_text_channel(
                name="ticket-logs",
                overwrites=logs_overwrites,
                topic="Logs for all ticket activities"
            )
            
            await logs_channel.send(embed=discord.Embed(
                title="Ticket Logs Channel",
                description="This channel will log all ticket activities.",
                color=discord.Color.green()
            ))
        
        # Create tickets channel
        tickets_channel = discord.utils.get(guild.text_channels, name="create-ticket")
        if not tickets_channel:
            tickets_channel = await guild.create_text_channel(
                name="create-ticket",
                topic="Create a support ticket here"
            )
            
            # Define the ticket type select dropdown
            class TicketTypeSelect(discord.ui.Select):
                def __init__(self):
                    options = [
                        discord.SelectOption(label="Support", description="Get help with an issue", emoji="❓"),
                        discord.SelectOption(label="Purchase", description="Questions about purchasing", emoji="💰")
                    ]
                    super().__init__(placeholder="Select ticket type...", min_values=1, max_values=1, options=options)
                    
                async def callback(self, interaction: discord.Interaction):
                    user = interaction.user
                    ticket_type = self.values[0]
                    
                    # Check if user already has a ticket
                    existing_channel = discord.utils.get(guild.text_channels, name=f"ticket-{user.name.lower()}")
                    if existing_channel:
                        await interaction.response.send_message("You already have a ticket open.", ephemeral=True)
                        return
                    
                    # Create the ticket with the selected type
                    await create_ticket(interaction, user, ticket_type)
            
            # Class for dropdown selection view
            class TicketTypeView(discord.ui.View):
                def __init__(self):
                    super().__init__(timeout=None)
                    self.add_item(TicketTypeSelect())
            
            # Create function to handle ticket creation
            async def create_ticket(interaction, user, ticket_type):
                # Get the staff role ID
                staff_role_id = int(os.environ.get("STAFF_ROLE_ID", "0"))
                
                # Create a private channel
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
                    guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
                }
                
                # Add staff role if it exists
                if staff_role_id:
                    role = guild.get_role(staff_role_id)
                    if role:
                        overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)
                
                # Create channel with ticket type in the name
                ticket_channel = await guild.create_text_channel(
                    name=f"ticket-{ticket_type.lower()}-{user.name}",
                    overwrites=overwrites,
                    topic=f"{ticket_type} ticket for {user.name}"
                )
                
                # Create first message with ticket information
                embed = discord.Embed(
                    title=f"{ticket_type} Ticket",
                    description=f"Thank you for opening a ticket, {user.mention}!",
                    color=discord.Color.blue(),
                    timestamp=discord.utils.utcnow()
                )
                embed.add_field(name="Type", value=ticket_type, inline=True)
                embed.add_field(name="Created By", value=user.mention, inline=True)
                embed.set_footer(text="A staff member will be with you shortly.")
                
                await ticket_channel.send(embed=embed)
                await interaction.response.send_message(f"Ticket created: {ticket_channel.mention}", ephemeral=True)
                
                # Log ticket creation
                log_embed = discord.Embed(
                    title="Ticket Created",
                    description=f"Ticket created by {user.mention}",
                    color=discord.Color.green(),
                    timestamp=discord.utils.utcnow()
                )
                log_embed.add_field(name="Channel", value=ticket_channel.mention, inline=True)
                log_embed.add_field(name="Type", value=ticket_type, inline=True)
                await logs_channel.send(embed=log_embed)
            
            # Create button for ticket creation
            button = Button(label="Create Ticket", style=discord.ButtonStyle.green)
            
            async def button_callback(interaction: discord.Interaction):
                # Show dropdown when button is clicked
                view = TicketTypeView()
                await interaction.response.send_message("Please select a ticket type:", view=view, ephemeral=True)
            
            button.callback = button_callback
            view = View()
            view.add_item(button)
            
            embed = discord.Embed(
                title="Support Tickets",
                description="Need help? Click the button below to create a ticket.",
                color=discord.Color.blue()
            )
            
            # Send the initial button view
            await tickets_channel.send(embed=embed, view=view)
        
        # Add close ticket command outside to avoid redefinition errors
        
        # Confirmation message
        setup_embed = discord.Embed(
            title="Ticket System Setup Complete",
            description="The ticket system has been set up successfully!",
            color=discord.Color.green()
        )
        setup_embed.add_field(name="Ticket Channel", value=tickets_channel.mention, inline=False)
        setup_embed.add_field(name="Logs Channel", value=logs_channel.mention, inline=False)
        if staff_role:
            setup_embed.add_field(name="Staff Role", value=staff_role.mention, inline=False)
        
        await ctx.send(embed=setup_embed)
        logger.info(f"Ticket system setup by {ctx.author}")


    # Add close ticket command
    @bot.command(name="close")
    async def close_ticket_command(ctx):
        """Close the current ticket channel."""
        if not ctx.channel.name.startswith("ticket-"):
            await ctx.send("This command can only be used inside a ticket channel.", delete_after=5)
            return
            
        await ctx.send("Closing ticket...")
        
        # Extract ticket type and user from channel name
        # Format: ticket-type-username
        channel_parts = ctx.channel.name.split('-')
        user_name = "unknown"
        ticket_type = "unknown"
        
        if len(channel_parts) >= 3:
            ticket_type = channel_parts[1]
            user_name = '-'.join(channel_parts[2:])  # Join the rest in case username has hyphens
        
        # Find logs channel
        logs_channel = discord.utils.get(ctx.guild.text_channels, name="ticket-logs")
        if logs_channel:
            log_embed = discord.Embed(
                title="Ticket Closed",
                description=f"Ticket for user `{user_name}` was closed by {ctx.author.mention}",
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow()
            )
            
            log_embed.add_field(name="Type", value=ticket_type.capitalize(), inline=True)
            await logs_channel.send(embed=log_embed)
        
        # Delete the channel
        await ctx.channel.delete()
