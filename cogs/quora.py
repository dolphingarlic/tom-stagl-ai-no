"""
Cog that responds to commands
"""

import os
from datetime import datetime

import discord
from discord.ext.commands import Cog, command


async def fetch_http(session, url, **kwargs):
    """Uses aiohttp to make http GET requests"""

    async with session.get(url, **kwargs) as response:
        return await response.json()


class Quora(Cog):
    def __init__(self, bot, session):
        self.bot = bot
        self.session = session
        self.start_time = datetime.now()

        self.prefix = 'tom pls give '
        if 'BOT_PREFIX' in os.environ:
            self.prefix = os.environ['BOT_PREFIX']

    @command(aliases=['source'])
    async def github(self, ctx):
        """
        Sends the link to the bot's GitHub repo
        """

        await ctx.send('https://github.com/dolphingarlic')

    @command(aliases=['stats'])
    async def about(self, ctx):
        """
        Sends information about the bot
        """

        info = await self.bot.application_info()
        embed = discord.Embed(
            title=f'{info.name}',
            description=f'{info.description}',
            colour=0x1aaae5,
        ).add_field(
            name='Guild Count',
            value=len(self.bot.guilds),
            inline=True
        ).add_field(
            name='User Count',
            value=len(self.bot.users),
            inline=True
        ).add_field(
            name='Uptime',
            value=f'{datetime.now() - self.start_time}',
            inline=True
        ).add_field(
            name='Latency',
            value=f'{round(self.bot.latency * 1000, 2)}ms',
            inline=True
        ).set_footer(text=f'Made by {info.owner}', icon_url=info.owner.avatar_url)

        await ctx.send(embed=embed)

    @command()
    async def help(self, ctx):
        """
        Sends a help message
        """

        embed = discord.Embed(
            title='Help',
            description='Help yourself. Easy. All The best',
            colour=0x41c03f
        ).add_field(
            name=f'`{self.prefix}advice`',
            value='Gives you GLOWING HOT advice Using GPT-2',
            inline=True
        ).add_field(
            name=f'`{self.prefix}about` or `{self.prefix}stats`',
            value='About me',
            inline=True
        ).add_field(
            name=f'`{self.prefix}invite`',
            value='Bot invite Link',
            inline=True
        ).add_field(
            name=f'`{self.prefix}help`',
            value='Shows this message',
            inline=True
        ).add_field(
            name=f'`{self.prefix}ping`',
            value='Check the bot\'s latency',
            inline=True
        ).add_field(
            name=f'`{self.prefix}github` or `{self.prefix}source`',
            value='Links to the bot\'s GitHub repo',
            inline=True
        )

        await ctx.send(embed=embed)

    @command()
    async def invite(self, ctx):
        """
        Sends a bot invite link
        """

        await ctx.send('https://discord.com/api/oauth2/authorize?client_id=729060467959660554&permissions=2048&scope=bot')

    @command()
    async def ping(self, ctx):
        """
        Checks latency
        """

        await ctx.send(f'Ice Hockey; {round(self.bot.latency * 1000, 2)}ms')

    @command()
    async def advice(self, ctx):
        """
        Requests advice from
        https://gpt2-os7x3hnhca-uc.a.run.app/
        """

        advice = await fetch_http(self.session, 'https://gpt2-os7x3hnhca-uc.a.run.app/')
        await ctx.send(advice['text'])
