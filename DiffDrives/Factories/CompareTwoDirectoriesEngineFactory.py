from DiffDrives.Fetchers.FetchDirectoryInfo import FetchDirectoryInfo
from DiffDrives.Engines.CompareTwoDirectories import CompareTwoDirectories

class CompareTwoDirectoriesEngineFactory(object):
    @staticmethod
    def getEngine():
        directoryInfoFetcher = FetchDirectoryInfo()
        return CompareTwoDirectories(directoryInfoFetcher)