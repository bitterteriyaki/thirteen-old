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

import redis.asyncio as redis


def create_cache():
    """Creates the Redis cache connection. This function is called in
    the :class:`bot.core.Thirteen` class.

    Returns
    -------
    :class:`redis.Redis`
        The Redis cache connection.
    """
    return redis.from_url(os.environ["REDIS_URL"], decode_responses=True)
