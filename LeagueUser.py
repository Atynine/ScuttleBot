from riotwatcher import RiotWatcher
from requests import HTTPError

class LeagueUser:
    region = 'NA1'
    leagueID = 0
    leagueName = 0
    lastGameID = 0
    __systemSettings = None
    __watcher = None
    __riotKey = None
    def __init__(self, leagueUsername, settings):
        self.__systemSettings = settings
        self.leagueName = leagueUsername
        self.leagueID = self.getUserID(leagueUsername)
        self.updateRiotKey()

    def updateRiotKey(self):
        if(self.__riotKey != self.__systemSettings.getRiotKey()):
            self.__riotKey = self.__systemSettings.getRiotKey()
            self.__watcher = RiotWatcher(self.__riotKey)
    def getUserID(self, leagueUsername):
        self.updateRiotKey()
        try:
            user = self.__watcher.summoner.by_name(self.region, leagueUsername)
        except HTTPError as err:
            return 0
        return str(user['id'])
    def getLeagueID(self):
        return self.leagueID
    async def updateGame(self):
        self.updateRiotKey()
        if(self.leagueID == 0):
            return 0
        try:
            currentGame = self.__watcher.spectator.by_summoner(self.region, self.leagueID)
        except HTTPError as err:
            if (str(err).startswith("403")):
                return -1
            return 0
        currentGame = currentGame['gameId']
        if(currentGame == self.lastGameID):
            return 0
        self.lastGameID = currentGame
        return self.lastGameID