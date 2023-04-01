import logging

import discord
from discord import app_commands
from discord.ext import commands

logging.basicConfig(level=logging.INFO)


class LeaveCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="leave", description="Leave the current voice channel.")
    async def leave(self, interaction: discord.Interaction) -> None:
        """Leave a voice channel."""
        if not interaction.guild:
            await interaction.response.send_message(
                "Cannot leave: I am not in a guild.",
                ephemeral=True,
            )
            return

        # If not in a voice channel, do nothing.
        if not interaction.guild.voice_client:
            await interaction.response.send_message(
                "Cannot leave: I am not in a voice channel.",
                ephemeral=True,
            )
            return

        # Stop audio playback.
        vc = interaction.guild.voice_client
        try:
            if vc.is_playing() or vc.is_paused():
                vc.stop()
        except Exception as e:
            # No method?
            pass

        await interaction.guild.voice_client.disconnect(force=False)
        await interaction.response.send_message(
            f"Left voice channel.",
            ephemeral=True,
        )
