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

import discord
from discord import app_commands
from discord.ext import commands
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from bot.utils.constants import GUILD_ID
from bot.utils.database import CurrencyUser


COIN_EMOJI = "\U0001fa99"


class Currency(commands.Cog):
    """Currency related commands. You can check your balance, give money
    to other users, and more.
    
    Attributes
    ----------
    bot: :class:`bot.core.Thirteen`
        The bot instance.
    """

    def __init__(self, bot):
        self.bot = bot

    async def insert_user(self, ctx):
        """Inserts a user into the database if they don't exist.
        
        Parameters
        ----------
        ctx: :class:`bot.utils.context.ThirteenContext`
            The context of the command.
        """
        member = ctx.kwargs.get("member") or ctx.author

        async with ctx.db.connect() as conn:
            insert_stmt = insert(CurrencyUser).values(id=member.id)
            stmt = insert_stmt.on_conflict_do_nothing()

            await conn.execute(stmt)
            await conn.commit()

    @commands.hybrid_command()
    @commands.before_invoke(insert_user)
    @app_commands.guilds(GUILD_ID)
    @app_commands.describe(member="The member to check the balance of.")
    async def balance(self, ctx, member: discord.Member = None):
        """Check your or another user's balance."""
        member = member or ctx.author

        async with ctx.db.connect() as conn:
            stmt = select(CurrencyUser).where(CurrencyUser.id == member.id)
            result = await conn.execute(stmt)

        user = result.first()

        message = f"{member.mention} has {user.balance} {COIN_EMOJI}."
        await ctx.reply(message)


async def setup(bot):
    await bot.add_cog(Currency(bot))
