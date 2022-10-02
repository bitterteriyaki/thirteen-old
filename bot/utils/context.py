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

from discord import Embed
from discord.ext.commands import Context


EMBED_COLOR = 0x2f3136


class ThirteenContext(Context):
    """A custom context class that inherits from the
    :class:`discord.ext.commands.Context` class.

    This class adds a few extra methods to the context class that
    are used throughout the bot.
    """

    @property
    def db(self):
        """Returns the current database connection engine.

        Returns
        -------
        :class:`sqlalchemy.ext.asyncio.AsyncEngine`
            The current database connection engine.
        """
        return self.bot.db

    def create_embed(self, content):
        """This method is a factory method that creates an embed with
        the given content. The embed is created with the default color
        and the content is set as the description.

        Parameters
        ----------
        content: :class:`str`
            The content of the embed.

        Returns
        -------
        :class:`discord.Embed`
            A new embed with the given content.
        """
        author = self.author

        embed = Embed(description=content, color=EMBED_COLOR)
        embed.set_author(name=author.name, icon_url=author.display_avatar.url)
        return embed

    async def reply(self, content):
        """This method is a wrapper around
        :meth:`discord.ext.context.Context.reply` method. It creates an
        embed with the content and the author's name and avatar. This
        method also does not mention the author.

        Parameters
        ----------
        content: :class:`str`
            The content of the embed.

        Returns
        -------
        :class:`discord.Message`
            The message sent.
        """
        embed = self.create_embed(content)
        return await super().reply(embed=embed, mention_author=False)
