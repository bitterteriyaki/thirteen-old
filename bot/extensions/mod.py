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

from typing import Literal

import discord
from discord.ext import commands
from discord import app_commands, Embed

from bot.utils.constants import GUILD_ID, EMBED_COLOR, LOG_CHANNEL_ID


REASONS = Literal[
    "Violação dos Termos de Serviço do Discord",
    "Divulgação de conteúdos sem autorização prévia",
    "Spamming, flooding ou qualquer outra forma de abuso",
    "Má convivência ou comportamento inapropriado",
    "Apelidos ou nomes de usuário inapropriados",
    "Desrespeitar o escopo dos canais ou servidor",
    "Burlamento de qualquer tipo de punição",
    "Mídias ou conteúdos inapropriados",
]

PUNISHMENTS_MAPPING = {
    "kick": "Membro expulso",
}


class Mod(commands.Cog):
    """Moderation related commands. These commands are only available to
    moderators.
    
    Attributes
    ----------
    bot: :class:`bot.core.Thirteen`
        The bot instance.
    """

    def __init__(self, bot):
        self.bot = bot

    @discord.utils.cached_property
    def log_channel(self):
        return self.bot.get_channel(LOG_CHANNEL_ID)

    async def log_action(self, ctx, member, reason):
        """Logs an action to the moderation-log channel.
        
        Parameters
        ----------
        ctx: :class:`bot.utils.context.ThirteenContext`
            The context of the command.
        member: :class:`discord.Member`
            The user that was punished.
        reason: :class:`str`
            The reason for the punishment.
        """
        author = ctx.author
        title = PUNISHMENTS_MAPPING[ctx.command.name]
        embed = Embed(title=title, color=EMBED_COLOR)
        embed.set_author(name=str(author), icon_url=author.display_avatar.url)
        embed.set_thumbnail(url=member.display_avatar.url)

        embed.add_field(name="Usuário punido", value=str(member), inline=False)
        embed.add_field(name="ID", value=f"`{member.id}`", inline=False)
        embed.add_field(name="Motivo", value=reason, inline=False)

        await self.log_channel.send(embed=embed)

    @commands.hybrid_command()
    @app_commands.guilds(GUILD_ID)
    async def kick(self, ctx, member: discord.Member, reason: REASONS):
        """Expulsa um usuário do servidor. Você precisa ter a permissão
        de expulsar membros para usar este comando. Você também precisa
        especificar um motivo para a expulsão.
        """
        try:
            # await member.kick()
            pass
        except discord.Forbidden:
            await ctx.reply("Eu não tenho permissão para expulsar este usuário.")
        else:
            await ctx.reply(f"**{member}** foi expulso do servidor.")
            await self.log_action(ctx, member, reason)



async def setup(bot):
    await bot.add_cog(Mod(bot))
