from os import path, makedirs, utime, sep
# object that handles interacting with the file system
class TestDataBuilder(object):
    # implementation of `touch` from https://stackoverflow.com/a/12654798/7520564
    def _touch(self, path):
        with open(path, 'a'):
            utime(path, None)

    def createFiles(self, context, filesToCreate):
        for f in filesToCreate:
            filePath = context + sep + f
            if not path.exists(filePath):
                print(f"FILE: {filePath}")
                self._touch(filePath)
    
    def createDir(self, context):
        if not path.exists(context):
            print(f"DIR: {context}")
            makedirs(context)