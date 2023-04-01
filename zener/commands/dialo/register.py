from discord.ext.commands import Bot
from .chat import chat_listener, ClearContextCommand


async def register(bot: Bot):
    bot.add_listener(chat_listener, "on_message")
    await bot.add_cog(ClearContextCommand(bot))
