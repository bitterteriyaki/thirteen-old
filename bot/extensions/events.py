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

import humanize
from discord.ext import commands
from discord.ext.commands.errors import *


class Events(commands.Cog):
    """Events cog. This cog contains all the events that the bot uses.

    Attributes
    ----------
    bot: :class:`bot.core.Thirteen`
        The bot instance.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            delta = humanize.precisedelta(error.retry_after, format="%0.0f")
            await ctx.reply(
                f"Você precisa esperar **{delta}** para usar este comando " \
                f"novamente."
            )


async def setup(bot):
    await bot.add_cog(Events(bot))
