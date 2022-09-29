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

from gino import Gino


db = Gino()


class CurrencyUser(db.Model):
    """A model representing a user in the currency system.

    Attributes
    ----------
    id: :class:`int`
        The user's ID.
    balance: :class:`int`
        The user's balance.
    """
    id = db.Column(db.BigInteger(), primary_key=True)
    balance = db.Column(db.BigInteger(), default=0, nullable=False)
