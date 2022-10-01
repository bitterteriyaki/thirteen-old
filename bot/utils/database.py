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

import os

from sqlalchemy import Column, BigInteger
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine


db = create_async_engine(os.environ["DATABASE_URL"])
Base = declarative_base()


class CurrencyUser(Base):
    """A model representing a user in the currency system.

    Attributes
    ----------
    id: :class:`int`
        The user's ID.
    balance: :class:`int`
        The user's balance.
    """
    __tablename__ = "currency"

    id = Column(BigInteger, primary_key=True)
    balance = Column(BigInteger, default=0, nullable=False)
