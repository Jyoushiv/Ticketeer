# Discord Ticket Bot

A simple Discord bot that allows users to create support tickets using buttons.

## Features

- Create tickets with a button click
- Private channels for support interactions
- Easy ticket management

## Commands

- `/ticket` - Creates a button for users to open tickets
- `/close` - Closes the current ticket channel (can only be used inside a ticket channel)
- 

## Setup

1. Make sure you have the Discord bot token ready
2. Set up your bot on the [Discord Developer Portal](https://discord.com/developers/applications)
   - Enable all Privileged Gateway Intents (Presence, Server Members, and Message Content)
   - Generate an invite link with the following permissions:
     - Manage Channels
     - Read/Send Messages
     - Read Message History
     - Manage Messages
     - Embed Links
     - Attach Files
     - Use Slash Commands
3. In the Secrets panel (lock icon) in your Replit project, add:
   - Key: `DISCORD_TOKEN`
   - Value: Your Discord bot token
4. Modify the `STAFF_ROLE_ID` in ticket_bot.py to match your staff role ID
5. Run the bot using terminal or Replit

## Keeping Your Bot Online 24/7

This bot includes a keep-alive server that responds to HTTP requests to prevent Replit from putting the bot to sleep. To ensure 24/7 uptime:

1. Use a service like UptimeRobot to ping your Replit URL every 5 minutes
2. Get your Replit URL by running the bot and looking at the webview URL

## Customization

- Change the STAFF_ROLE_ID to match your server's staff role
- Modify ticket channel names and messages in the code
- Add additional commands as needed

## Troubleshooting (in Replit)

- If the bot doesn't connect, check if your token is correctly set in the Secrets tab
- Make sure you've invited the bot to your server with the correct permissions
- Check the logs in the Replit console for any error messages
