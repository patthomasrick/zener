import logging

import discord
from discord.ext import commands

from zener.commands.dialo.register import register as register_dialo
from zener.commands.util.register import register as register_util
from zener.commands.youtube.register import register as register_youtube
from zener.config import Config

logging.basicConfig(level=logging.INFO)

# Oauth https://discord.com/api/oauth2/authorize?client_id=967217448384331776&permissions=8&scope=bot


class ZenerBot(commands.Bot):
    def __init__(self):
        # Ignore intents that we don't use.
        intents = discord.Intents.default()
        intents.typing = False
        intents.presences = False
        intents.integrations = True
        intents.message_content = True

        super().__init__(command_prefix="!", intents=intents)


if __name__ == "__main__":
    logging.info("--- ZENER ---")
    logging.info("Starting...")

    # Load config from file.
    logging.info("Loading config from config.ini...")
    config = Config("config.ini")
    token = config.secret
    # Basic validation on token.
    if len(token) == 0 or token == "your_secret_token":
        logging.error(
            "Error loading config - secret bot token is invalid. Be sure to set it."
        )
        exit(1)

    # Create the client.
    client = ZenerBot()

    # On quit, leave all voice channels.
    @client.event
    async def on_disconnect(self):
        logging.info("Disconnecting...")
        for channel in client.voice_clients:
            await channel.disconnect(force=False)

    # Register commands.
    @client.event
    async def on_ready():
        logging.info(f"Logged in as {client.user}")

        logging.info("Registering commands.")
        await register_youtube(client)
        await register_util(client)
        await register_dialo(client)

        # Sync commands on guilds.
        logging.info("Syncing commands on guilds.")
        for guild in client.guilds:
            client.tree.copy_global_to(guild=guild)
            commands = await client.tree.sync(guild=guild)
            logging.info(f"Synced {len(commands)} commands on {guild.name}.")

    # Run the client.
    logging.info("Starting client.")
    client.run(token)
