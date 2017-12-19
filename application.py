import asyncio
import discord
from Settings import Settings
from discord.ext import commands
from LeagueUserRepository import LeagueUserRepository


bot = commands.Bot(command_prefix='!')

systemSettings = Settings()
leagueUsers = LeagueUserRepository(systemSettings)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

async def my_background_task():
    global systemSettings
    await bot.wait_until_ready()
    counter = 0
    while not bot.is_closed:
        counter += 1
        if(systemSettings.isPaused() == False):
            await leagueUsers.checkAll(bot)
        await asyncio.sleep(systemSettings.getUpdateInterval())


@bot.command(pass_context=True, aliases={'r'})
async def register(ctx, *, message : str):
    global systemSettings
    if(systemSettings.isPaused()==True):
        return
    userId = ctx.message.author.id
    #Attempt to register the user
    if (await leagueUsers.addUser(userId, message) == 0):
        #If the league ID does not exist, adding user failed
        await bot.send_message(ctx.message.channel, 'Failed to register with username ' + message)
        await log(getUserMention(userId) + ' failed to register with username ' + message)
        return
    #If the league ID does exist, register it to the user and message them saying they were registered
    await bot.send_message(ctx.message.channel, 'Registered as (NA)' + message)
    await log(getUserMention(userId) + ' registered as (NA)' + message)
    #Delete the message for a cleaner chat
    #TODO Fix error when trying to delete a message in DMs
    await bot.delete_message(ctx.message)
    return

@bot.group(pass_context=True, aliases={'s'})
async def settings(ctx):
    global systemSettings
    if(int(ctx.message.author.id) != 154798484996751361):
        ctx.invoked_subcommand = None
        return
    if ctx.invoked_subcommand is None:
        #TODO Make toString method in Settings
        await log('Current Settings:\nDebugChannel-'+systemSettings.getDebugChannel()+
                  "\nOutputChannel-"+systemSettings.getOutputChannel()+
                  "\nRiot API Key-"+systemSettings.getRiotKey()+
                  "\nPaused-"+str(systemSettings.isPaused()))
    await bot.delete_message(ctx.message)
@settings.command()
async def help():
    await bot.say('List of valid subcommands: setRiotKey, setDebugChannel, setOutputChannel, pause, resume')
@settings.command(pass_context=True, aliases={'setRiotKey'})
async def setriotkey(ctx, message: str = None):
    global systemSettings
    if (systemSettings.isPaused==True):
        return
    if (message == None):
        await bot.say('setRiotKey requires a key \'!settings setRiotKey {key}\'')
        return
    systemSettings.setRiotKey(message)
    await log(getUserMention(ctx.message.author.id) + ' changed Riot API key to ' + message)
@settings.command(pass_context=True, aliases={'setDebugChannel'})
async def setdebugchannel(ctx, message: str = None):
    global systemSettings
    if (systemSettings.isPaused==True):
        return
    if (message == None):
        await bot.say('setDebugchannel requires a channel \'!settings setDebugChannel {channel}\'')
        return
    systemSettings.setDebugChannel(message)
    await log(getUserMention(ctx.message.author.id) + ' changed debug channel to ' + message)
@settings.command(pass_context=True, aliases={'setOutputChannel'})
async def setoutputchannel(ctx, message: str = None):
    global systemSettings
    if (systemSettings.isPaused==True):
        print(message)
        return
    if(message == None):
        await bot.say('setOutputChannel requires a channelID \'!settings setOutputChannel {channel}\'')
        return
    systemSettings.setOutputChannel(message)
    await log(getUserMention(ctx.message.author.id) + ' changed output channel to ' + message)
@settings.command(pass_context=True, aliases={'p'})
async def pause(ctx, message: str = None):
    global systemSettings
    systemSettings.pause()
    await log(getUserMention(ctx.message.author.id) + ' paused the bot')
@settings.command(pass_context=True, aliases={'r'})
async def resume(ctx, message: str = None):
    global systemSettings
    systemSettings.resume()
    await log(getUserMention(ctx.message.author.id) + ' resumed the bot')


async def log(message : str):
    logChannel = discord.Object(id=systemSettings.getDebugChannel())
    return await bot.send_message(logChannel, message)
def getUserMention(userId):
    return '<@'+userId+'>'



bot.loop.create_task(my_background_task())
bot.run(systemSettings.getDiscordKey())