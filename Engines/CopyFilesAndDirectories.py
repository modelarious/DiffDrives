# copy2 will copy metadata of the file
from shutil import copy2, copytree
from os import path

class CopyFilesAndDirectories:

    def _getSourcePath(self, sourcePath, pathA, pathB):
        return sourcePath.replace(pathB, pathA)
    
    def copyFilesAndDirectories(self, pathA, pathB, fileAndDirectoryPaths):
        for destinationFilePath in fileAndDirectoryPaths.getFiles():
            sourceFilePath = self._getSourcePath(destinationFilePath, pathA, pathB)
            print(f"copying {sourceFilePath} to {destinationFilePath}")
            copy2(sourceFilePath, destinationFilePath)
        
        for destinationDirectoryPath in fileAndDirectoryPaths.getDirectories():
            sourceDirectoryPath = self._getSourcePath(destinationDirectoryPath, pathA, pathB)
            print(f"copying {sourceDirectoryPath} to {destinationDirectoryPath}")
            copytree(sourceDirectoryPath, destinationDirectoryPath, copy_function=copy2)

