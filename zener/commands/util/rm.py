import logging

import discord
from discord import Message, app_commands
from discord.ext import commands

logging.basicConfig(level=logging.INFO)


# Define a simple View that gives us a confirmation menu
class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.state = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        logging.info("Confirm button pressed.")
        self.state = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        logging.info("Cancel button pressed.")
        self.state = False
        self.stop()


class Rm(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    group = app_commands.Group(name="rm", description="Removal commands.")

    @group.command(
        description="Remove messages by exact text match.",
    )
    async def messages_by_exact_text(
        self, interaction: discord.Interaction, pattern: str
    ) -> None:
        """Delete messages whose content matches the given pattern.

        Args:
            interaction (discord.Interaction): Interaction.
            pattern (str): Pattern to match against.
        """
        logging.info(f"Searching for messages with text '{pattern}' for deletion.")

        # Get the sender's text channel.
        channel = interaction.channel
        if not channel:
            await interaction.response.send_message(
                "Cannot remove messages: not in a channel.", ephemeral=True
            )
            return

        # Make sure the sender is an admin.
        if not await self.ensure_admin(interaction):
            await interaction.response.send_message(
                "Cannot remove messages: insufficient permissions.",
                ephemeral=True,
            )
            return

        # Get messages from the channel.
        to_delete = []
        message: Message
        async for message in channel.history(limit=None):
            if message.content == pattern:
                to_delete.append(message)

        await self.confirm_delete(interaction, to_delete)

    @group.command(
        description="Remove messages that start with the query.",
    )
    async def messages_by_start_text(
        self, interaction: discord.Interaction, pattern: str
    ) -> None:
        """Delete messages whose content starts with the given pattern.

        Args:
            interaction (discord.Interaction): Interaction.
            pattern (str): Pattern to match against.
        """
        logging.info(
            f"Searching for messages with text starting with '{pattern}' for deletion."
        )

        # Get the sender's text channel.
        channel = interaction.channel
        if not channel:
            await interaction.response.send_message(
                "Cannot remove messages: not in a channel.", ephemeral=True
            )
            return

        # Make sure the sender is an admin.
        if not await self.ensure_admin(interaction):
            await interaction.response.send_message(
                "Cannot remove messages: insufficient permissions.",
                ephemeral=True,
            )
            return

        # Get messages from the channel.
        to_delete = []
        message: Message
        async for message in channel.history(limit=None):
            if message.content.startswith(pattern):
                to_delete.append(message)

        await self.confirm_delete(interaction, to_delete)

    async def ensure_admin(self, interaction: discord.Interaction) -> bool:
        """Ensure the sender is an admin.

        Args:
            interaction (discord.Interaction): Interaction.
        """
        # Make sure the sender is an admin.
        if interaction.user and interaction.user.guild_permissions:
            perms: discord.Permissions = interaction.user.guild_permissions
            if perms.manage_messages or perms.administrator:
                return True
        return False

    async def confirm_delete(self, interaction: discord.Interaction, to_delete: list):
        # We create the view and assign it to a variable so we can wait for it later.
        view = Confirm()
        await interaction.response.send_message(
            f"Do you want to delete {len(to_delete)} messages?",
            view=view,
            ephemeral=True,
        )
        # Wait for the View to stop listening for input...
        await view.wait()

        # Test if the user confirmed the deletion.
        if view.state is True:
            # Delete the messages.
            await interaction.edit_original_message(
                content=f"Deleting {len(to_delete)} messages.", view=None
            )
            for message in to_delete:
                await message.delete()
            await interaction.edit_original_message(
                content=f"Deleted {len(to_delete)} messages.", view=None
            )
            logging.info(f"Deleted {len(to_delete)} messages.")
        else:
            await interaction.edit_original_message(
                content="Cancelled deletion.", view=None
            )
            logging.info("Cancelled deletion.")
