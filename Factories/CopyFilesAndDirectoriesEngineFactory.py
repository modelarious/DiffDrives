from Engines.CopyFilesAndDirectories import CopyFilesAndDirectories

class CopyFilesAndDirectoriesEngineFactory(object):
    @staticmethod
    def getEngine():
        return CopyFilesAndDirectories()