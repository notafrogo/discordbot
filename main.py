#imports
import discord
import os
from discord.ext import commands

#define client
client = commands.Bot(command_prefix='.')


#startup info
@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game(''))





"""commands"""    

@client.command()
@commands.has_permissions(manage_channels=True)
#clear (amount)
async def clear(ctx, amount=100):
    await ctx.channel.purge(limit=amount)

@client.command()
@commands.has_permissions(manage_channels=True)
#clearall
async def clearall(ctx):
    await ctx.channel.purge()

@client.command()
@commands.has_permissions(kick_members=True)
#ban member
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    embedban = discord.Embed(
        title='Banned {}'.format(member),
        description='Reason given: {}'.format(reason),
        colour=discord.Colour.red()
    )
    embedban.set_thumbnail(url=member.avatar_url)
    embedban.set_footer(text='The Ban Hammer was dropped on {}.'.format(member))
    await ctx.channel.send(embed=embedban)


@client.command()
@commands.has_permissions(kick_members=True)
#unban member
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            embedunban = discord.Embed(
                title='Unbanned {}'.format(member),
                colour=discord.Colour.green()
            )
    await ctx.channel.send(embed=embedunban)


@client.command()
@commands.has_permissions(kick_members=True)
#kick member
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    embedkick = discord.Embed(
        title= '{}'.format(member),
        description='Reason given: {}'.format(reason),
        colour=discord.Colour.red()
    )
    embedkick.set_thumbnail(url=member.avatar_url)
    embedkick.set_footer(text='Get kicked {}.'.format(member))
    await ctx.channel.send(embed=embedkick)


@client.command()
@commands.has_permissions(administrator=True)
#set game
async def play(ctx, game):
    await client.change_presence(activity=discord.Game(game))


@client.command()
#info
async def info(ctx, *, member: discord.Member):
    fmt1 = '{0}'
    fmt2 = 'Joined on {0.joined_at} and has {1} roles.'
    embedinfo = discord.Embed(
        title=fmt1.format(member, len(member.roles)),
        description=fmt2.format(member, len(member.roles)),
        colour=discord.Colour.blue()
    )
    embedinfo.set_footer(text=fmt1.format(member, len(member.roles)))
    embedinfo.set_thumbnail(url=member.avatar_url)
    await ctx.channel.send(embed=embedinfo)


@info.error
#info error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embedinfoerror = discord.Embed(
            description='I could not find that member...',
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embedinfoerror)


#run bot

"""run"""
token = os.environ['token']
client.run(token)