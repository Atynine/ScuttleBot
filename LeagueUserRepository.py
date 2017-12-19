import discord
import asyncio
from LeagueUser import LeagueUser

waitTime = 10

class LeagueUserRepository:
    __systemSettings = None
    __users__ = {};
    __showedAPIKeyMessage = True
    def __init__(self, settings):
        self.__systemSettings = settings
    async def checkAll(self, bot):
        for discordID, user in self.__users__.items():
            await self.isInNewGame(bot,user,discordID)
    async def addUser(self, discordID, leagueUsername):
        user = LeagueUser(leagueUsername, self.__systemSettings)
        if(user.leagueID == 0):
            return 0
        self.__users__[discordID] = user
        return 1
    async def isInNewGame(self, bot, user, discordID):
        newGameID = await user.updateGame()
        if(newGameID >= 1):
            await asyncio.sleep(waitTime)
            await self.__systemSettings.output(bot, '<@'+discordID+'> Here are your match details')
            msg = await self.__systemSettings.output(bot, '!b live NA ' + user.leagueName)
            #Delete baron bot call message for a cleaner chat
            await bot.delete_message(msg)
            self.__showedAPIKeyMessage = False
        elif(newGameID == -1):
            if(self.__showedAPIKeyMessage==False):
                await self.__systemSettings.log(bot, "API Key Revoked https://developer.riotgames.com/")
                self.__showedAPIKeyMessage = True
        else:
            self.__showedAPIKeyMessage = False