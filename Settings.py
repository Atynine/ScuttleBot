import json
import os
import discord


class Settings:
    __settings = {}
    __settings_directory = 'config/'
    __settings_filename = 'settings.json'
    __riotAPIKey = 'riotKey'
    __debugChannel = 'debugChannel'
    __discordAPIKey = 'discordKey'
    __updateInterval = 'updateInterval'
    __outputChannel = 'outputChannel'
    __paused = False


    def __init__(self):
        #Create config directory if it does not exist
        if not os.path.exists(self.__settings_directory):
            os.makedirs(self.__settings_directory)
            return
        #Read previously saved settings
        with open(self.__settings_directory+self.__settings_filename, 'r') as f:
            self.__settings = json.load(f)
        return
    def __save(self):
        with open(self.__settings_directory+self.__settings_filename, 'w') as f:
            json.dump(self.__settings, f)
        return


    async def output(self, bot, message):
        channel = discord.Object(id=self.getOutputChannel())
        return await bot.send_message(channel, message)
    async def log(self, bot, message):
        channel = discord.Object(id=self.getDebugChannel())
        return await bot.send_message(channel, message)

    def pause(self):
        self.__paused = True
    def resume(self):
        self.__paused = False
    def isPaused(self):
        return self.__paused
    def getDiscordKey(self):
        return self.__settings[self.__discordAPIKey]
    def getRiotKey(self):
        return self.__settings[self.__riotAPIKey]
    def getDebugChannel(self):
        return self.__settings[self.__debugChannel]
    def getUpdateInterval(self):
        return self.__settings[self.__updateInterval]
    def getOutputChannel(self):
        return self.__settings[self.__outputChannel]
    def setDiscordKey(self, key):
        self.__settings[self.__discordAPIKey] = key
        self.__save()
    def setRiotKey(self, key):
        self.__settings[self.__riotAPIKey] = key
        self.__save()
    def setDebugChannel(self, channel):
        self.__settings[self.__debugChannel] = channel
        self.__save()
    def setUpdateInterval(self, interval):
        self.__settings[self.__updateInterval] = interval
        self.__save()
    def setOutputChannel(self, channel):
        self.__settings[self.__outputChannel] = channel
        self.__save()