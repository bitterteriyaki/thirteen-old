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


INTENTS = discord.Intents.all()


class Thirteen(commands.Bot):
    """The main bot class. This class inherits from the
    :class:`discord.ext.commands.Bot` class.
    
    Attributes
    ----------
    is_first_run: :class:`bool`
        Whether or not the bot is running for the first time.
    """

    def __init__(self):
        super().__init__(command_prefix=get_prefix, intents=INTENTS)

        self.is_first_run = True

    async def on_ready(self):
        if self.is_first_run:
            print(f"[yellow]✦ Bot is ready. Logged in as {self.user}.[/]")
            print(f"[yellow]✦ Running with {len(self.users)} users.[/]")

            self.is_first_run = False

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
