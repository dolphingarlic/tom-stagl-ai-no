"""
Tom StaglAIno

A Discord bot that impersonates Tom Stagliano using gpt2
"""

import asyncio
import os
import logging

from discord import Activity, ActivityType
from discord.ext.commands import Bot, when_mentioned_or
import aiohttp

from cogs.quora import Quora

async def main():
    logging.basicConfig(level=logging.INFO)

    prefix = os.environ.get('BOT_PREFIX', 'tom pls give ')

    bot = Bot(
        command_prefix=when_mentioned_or(prefix),
        help_command=None,
        activity=Activity(type=ActivityType.watching, name='my MIT acceptance letter | `tom pls give help` for help')
    )

    async with aiohttp.ClientSession() as session:
        bot.add_cog(Quora(bot, session))

        await bot.start(os.environ['DISCORD_TOKEN'])


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        loop.close()
