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

import random

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Author
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert

from bot.utils.constants import GUILD_ID
from bot.utils.database import CurrencyUser


COIN_EMOJI = "\U0001fa99"


class Currency(commands.Cog):
    """Currency related commands. You can check your balance, give
    credits to other users, and more.
    
    Attributes
    ----------
    bot: :class:`bot.core.Thirteen`
        The bot instance.
    """

    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        async with self.bot.db.connect() as conn:
            users = await conn.execute(select(CurrencyUser))

        for user_id, balance in users.all():
            await self.bot.cache.setnx(f"currency:{user_id}:balance", balance)

    async def add_credits(self, user_id, amount):
        """Adds credits to a user. If the user doesn't exist in the
        database, they will be inserted.

        Parameters
        ----------
        user_id: :class:`int`
            The user ID.
        amount: :class:`int`
            The amount of credits to add.
        """
        async with self.bot.db.connect() as conn:
            insert_stmt = insert(CurrencyUser).values(id=user_id)
            stmt = insert_stmt.on_conflict_do_nothing()

            await conn.execute(stmt)
            await conn.commit()

        async with self.bot.db.connect() as conn:
            await conn.execute(
                update(CurrencyUser)
                .where(CurrencyUser.id == user_id)
                .values(balance=CurrencyUser.balance + amount)
            )
            await conn.commit()

        await self.bot.cache.incrby(f"currency:{user_id}:balance", amount)

    @commands.hybrid_command()
    @app_commands.guilds(GUILD_ID)
    @app_commands.describe(member="O membro para verificar o saldo.")
    async def balance(self, ctx, member: discord.Member = Author):
        """Verifique seu saldo atual (ou a de outro membro)."""
        balance = await ctx.cache.get(f"currency:{member.id}:balance") or 0
        word = "Você" if member == ctx.author else member.mention
        await ctx.reply(f"{word} tem **{balance} {COIN_EMOJI}**.")

    @commands.hybrid_command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    @app_commands.guilds(GUILD_ID)
    @app_commands.describe(member="O membro a quem dar os créditos.")
    async def daily(self, ctx, member: discord.Member = Author):
        """Colete seus créditos diários ou dê a outro usuário."""
        amount = random.randint(25, 50)
        await self.add_credits(member.id, amount)

        word = "Você" if member == ctx.author else member.mention
        await ctx.reply(f"{word} coletou **{amount} {COIN_EMOJI}**.")

    @commands.hybrid_command()
    @app_commands.guilds(GUILD_ID)
    @app_commands.describe(member="O membro a quem transferir os créditos.")
    async def transfer(
        self,
        ctx,
        member: discord.Member,
        amount: app_commands.Range[int, 0, None],
    ):
        """Transfira créditos para outro usuário."""
        if member == ctx.author:
            return await ctx.reply(
                "Você não pode transferir créditos para si mesmo."
            )

        if member.bot:
            return await ctx.reply(
                "Você não pode transferir créditos para um bot."
            )

        balance = await ctx.cache.get(f"currency:{ctx.author.id}:balance") or 0

        if amount > balance:
            return await ctx.reply("Você não tem créditos suficientes.")

        await self.add_credits(member.id, amount)
        await self.add_credits(ctx.author.id, -amount)

        await ctx.reply(
            f"Você transferiu **{amount} {COIN_EMOJI}** para {member.mention}."
        )


async def setup(bot):
    await bot.add_cog(Currency(bot))
