"""
Copyright (C) 2022 kyomi

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import traceback

import discord
from discord.ext import commands
from rich import print

from bot.utils.extensions import get_extensions
from bot.utils.context import ThirteenContext
from bot.utils.database import create_engine
from bot.utils.cache import create_cache


INTENTS = discord.Intents.all()


class Thirteen(commands.Bot):
    """The main bot class. This class inherits from the
    :class:`discord.ext.commands.Bot` class.
    
    Attributes
    ----------
    db: :class:`sqlalchemy.ext.asyncio.AsyncEngine`
        The database connection engine.
    cache: :class:`redis.Redis`
        The Redis cache connection.
    is_first_run: :class:`bool`
        Whether or not the bot is running for the first time.
    """

    def __init__(self):
        super().__init__(command_prefix=get_prefix, intents=INTENTS)

        self.db = create_engine()
        self.cache = create_cache()
        self.is_first_run = True

    async def on_ready(self):
        if self.is_first_run:
            print(f"[yellow]✦ Bot is ready. Logged in as {self.user}.[/]")
            print(f"[yellow]✦ Running with {len(self.users)} users.[/]")

            self.is_first_run = False

    async def on_message(self, message):
        # Ignore messages from webhooks and bots.
        if not isinstance(message.author, discord.Member):
            return
        
        if message.author.bot:
            return

        self.dispatch("regular_message", message)
        await self.process_commands(message)

    async def get_context(self, message):
        return await super().get_context(message, cls=ThirteenContext)

    async def setup_hook(self):
        for extension in get_extensions():
            try:
                await self.load_extension(extension)
            except Exception as e:
                exc = traceback.format_exception(type(e), e, e.__traceback__)
                formatted_exc = "".join(exc)

                print(f"[red]✦ Failed to load extension [u]{extension}[/]:[/]")
                print(f"[dim]{formatted_exc}[/]", end="")
            else:
                print(f"[green]✦ Loaded extension [u]{extension}[/].")


async def get_prefix(bot, message):
    """Returns the prefix used for message commands.

    Parameters
    ---------
    bot: :class:`Thirteen`
        The bot instance.
    message: :class:`discord.Message`
        The message that invoked the command.

    Returns
    -------
    :class:`str`
        The prefix used for message commands.

    Notes
    -----
    This command will be customizable in the future for user specific
    prefixes.
    """
    return "13!"
