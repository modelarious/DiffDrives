'''
- getPath() returns the path of the current directory
- getDirs() returns a set of all subdirectories in the current directory
- getFiles() returns a set of all files in the current directory with the exclusion of anything in "skippedFiles"
'''
class DirectoryInfo(object):
    def __init__(self, path, dirs, files):
        #various files that don't need to be considered
        skippedFiles = [".DS_Store"]
        skippedDirectories = [".fseventsd", '.Spotlight-V100', '.Trashes', '.DocumentRevisions-V100', '.TemporaryItems']
        
#         ignoreFileRegex = '._'

        self.path = path
        self.containedDirectories = self._skip(dirs, skippedDirectories)
        self.containedFiles = self._skip(files, skippedFiles)

    def _skip(self, array, skipValues):
        return set((v for v in array if v not in skipValues))
        #return set((v for v in array if v not in skipValues and not v.startswith(self.ignoreFileRegex)))

    def getPath(self):
        return self.path

    def getDirs(self):
        return self.containedDirectories

    def getFiles(self):
        return self.containedFiles
