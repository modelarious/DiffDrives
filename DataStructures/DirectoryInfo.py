'''
- getPath() returns the path of the current directory
- getDirs() returns a set of all subdirectories in the current directory
- getFiles() returns a set of all files in the current directory with the exclusion of anything in "skippedFiles"
'''
class DirectoryInfo(object):
    def __init__(self, path, dirs, files):
        #various files that don't need to be considered
        skippedFiles = [".DS_Store"]

        self.path = path
        self.containedDirectories = set(dirs)
        self.containedFiles = set((f for f in files if f not in skippedFiles))

    def getPath(self):
        return self.path

    def getDirs(self):
        return self.containedDirectories

    def getFiles(self):
        return self.containedFiles
