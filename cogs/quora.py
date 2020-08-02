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

        await ctx.send('https://github.com/dolphingarlic/tom-stagl-ai-no')

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
            name=f'`{self.prefix}advice` or `{self.prefix}wisdom`',
            value='Gives you GLOWING HOT advice Using GPT-2',
            inline=True
        ).add_field(
            name=f'`{self.prefix}about` or `{self.prefix}stats`',
            value='About me (Tom Stagliano - MIT class of \'76)',
            inline=True
        ).add_field(
            name=f'`{self.prefix}invite`',
            value='Bot invite Link',
            inline=True
        ).add_field(
            name=f'`{self.prefix}help`',
            value='Shows This message (did I mention I Went To MIT?)',
            inline=True
        ).add_field(
            name=f'`{self.prefix}ping`',
            value='Check the bot\'s Latency',
            inline=True
        ).add_field(
            name=f'`{self.prefix}github` or `{self.prefix}source`',
            value='Links to the Bot\'s ~~MIT~~ GitHub repo',
            inline=True
        )

        await ctx.send(embed=embed)

    @command(aliases=['topgg'])
    async def invite(self, ctx):
        """
        Sends a bot invite link
        """

        await ctx.send('https://top.gg/bot/729060467959660554')

    @command()
    async def ping(self, ctx):
        """
        Checks latency
        """

        await ctx.send(f'Ice Hockey; {round(self.bot.latency * 1000, 2)}ms')

    @Cog.listener()
    async def on_guild_join(self, guild):
        """
        Sends a nice message when added to a new server
        """

        embed = discord.Embed(
            title='Hi, I\'m Tom StaglAIno',
            description=f'To get started, type `{self.prefix} help`.',
            colour=0x2ac99e
        ).add_field(
            name='Who am I?',
            value='~~I\'m Tom StaglAIno, can\'t you read?~~\n'
            + 'I\'m a bot made with GPT-2 trained on Tom Stagliano\'s Quora answers.\n'
            + '(I may be a bit slow to respond because of GPT-2 but please be patient.)',
            inline=False
        ).add_field(
            name='Don\'t forget your GLOWING HOT LETTERS OF RECOMMENDATION!',
            value=':envelope:',
            inline=False
        ).set_footer(text='Did I mention I went to MIT?')
        await guild.system_channel.send(embed=embed)

    @command(aliases=['wisdom'])
    async def advice(self, ctx, prefix=''):
        """
        Requests advice from
        https://gpt2-os7x3hnhca-uc.a.run.app/
        """

        advice = await fetch_http(self.session, f'https://gpt2-os7x3hnhca-uc.a.run.app/?prefix={prefix}')
        await ctx.send(f'{advice["text"]}\n\nEasy. Good Luck.')
