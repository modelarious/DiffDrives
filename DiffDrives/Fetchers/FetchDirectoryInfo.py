from DiffDrives.Fetchers.FetchDirectoryInfoAbstract import FetchDirectoryInfoAbstract
from DiffDrives.DataStructures.DirectoryInfo import DirectoryInfo
from os import walk
'''
Walks through the directory structure and generates tuples of three entries 
that represents where we are in the file system:
(
	'/path/to/directory', 
	['dirs', 'in', 'this', 'directory'], 
	['files.txt', 'in.txt', 'this.txt', 'directory.txt']
)
'''
class FetchDirectoryInfo(FetchDirectoryInfoAbstract):
	def getDirectoryInfo(self, path):
		try:
			return DirectoryInfo(*next(walk(path)))
		except StopIteration:
			return None