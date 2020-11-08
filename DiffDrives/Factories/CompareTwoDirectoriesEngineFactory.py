from Fetchers.FetchDirectoryInfo import FetchDirectoryInfo
from Engines.CompareTwoDirectories import CompareTwoDirectories

class CompareTwoDirectoriesEngineFactory(object):
    @staticmethod
    def getEngine():
        directoryInfoFetcher = FetchDirectoryInfo()
        return CompareTwoDirectories(directoryInfoFetcher)