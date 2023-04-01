import logging

import discord
import requests
from discord import Message, app_commands
from discord.ext import commands

logging.basicConfig(level=logging.INFO)


async def chat_listener(message: Message) -> None:
    # Make sure the message mentions the bot.
    if (
        not message.mentions
        or not message.guild
        or message.guild.me not in message.mentions
    ):
        return

    logging.info(f"Received message: {message.content}")

    # Send a POST request to dialo:5000 with data user_input=message
    request = requests.post("http://dialo:5000", data={"user_input": message.content})
    if request.status_code != 200:
        logging.error(f"Error from dialo: {request.status_code}, {request.text}")
        await message.reply("ERROR: Something went wrong. Please try again.")
        return

    reply = request.json().get("response", "ERROR: Problem getting response.")
    if reply == "":
        reply = "ERROR: No response from dialo."

    if reply.startswith("ERROR:"):
        logging.error(f"Error from dialo: {reply}")

    logging.info(f"Sending reply: {reply}")
    await message.reply(reply)


class ClearContextCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="clearcontext", description="Clear the chat context.")
    async def clearcontext(self, interaction: discord.Interaction) -> None:
        request = requests.delete("http://dialo:5000")

        if request.status_code != 200:
            await interaction.response.send_message(
                "ERROR: Something went wrong. Please try again.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            "Context cleared.",
            ephemeral=True,
        )
