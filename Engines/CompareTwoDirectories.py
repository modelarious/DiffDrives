from os import sep
from DataStructures.DiffDataStructure import DiffDataStructure
from Logging import printSTATUS, printDEBUG

class CompareTwoDirectories(object):
	def __init__(self, directoryInfoFetcher):
		self.directoryInfoFetcher = directoryInfoFetcher

	def compare(self, pathA, pathB):
		self.dataStorage = DiffDataStructure()
		self._compareRecurse(pathA, pathB)
		return self.dataStorage
	
	def _pathFrom(self, pathStart, nextLevel):
		return pathStart + sep + nextLevel

	def _getResultsOfSetOperations(self, directoryInfoA, directoryInfoB):
		dirsA, filesA = directoryInfoA.getDirs(), directoryInfoA.getFiles()
		dirsB, filesB = directoryInfoB.getDirs(), directoryInfoB.getFiles()

		# we want to recurse into any directories that exist in B and in A
		unionDirs = [x for x in dirsB if x in dirsA]
		printSTATUS("dirs in B that are also in A:", unionDirs)

		dirsInAbutNotB = [x for x in dirsA if x not in dirsB]
		printSTATUS("dirs in A but not in B:", dirsInAbutNotB)

		filesInAbutNotInB = [x for x in filesA if x not in filesB]
		printSTATUS("files in A but not in B:", filesInAbutNotInB)

		return unionDirs, dirsInAbutNotB, filesInAbutNotInB
	
	def _trackDifferencesAndCalculateNextCandidates(self, directoryInfoA, directoryInfoB):
		unionDirs, dirsInAbutNotB, filesInAbutNotInB = self._getResultsOfSetOperations(directoryInfoA, directoryInfoB)

		# add the path to all files and dirs that were missing
		pathB = directoryInfoB.getPath()
		dirExtension = [self._pathFrom(pathB, x) for x in dirsInAbutNotB]
		fileExtension = [self._pathFrom(pathB, x) for x in filesInAbutNotInB] 

		# track all the missing files and dirs
		self.dataStorage.trackDirs(dirExtension)
		self.dataStorage.trackFiles(fileExtension)

		return unionDirs

	def _compareRecurse(self, pathA, pathB):
		printSTATUS("calling compareRecurse with", pathA, pathB)

		directoryInfoA = self.directoryInfoFetcher.getDirectoryInfo(pathA)
		directoryInfoB = self.directoryInfoFetcher.getDirectoryInfo(pathB)

		#We're only looking for what's in A that isn't in B, so we don't care if children of B is None, we only worry about when we've exhausted children of A
		if directoryInfoA == None:
			printDEBUG("Exhausted A, returning diff dict")
			return None

		nextCandidates = self._trackDifferencesAndCalculateNextCandidates(directoryInfoA, directoryInfoB)
		
		for childofBoth in nextCandidates:
			newPathA = self._pathFrom(pathA, childofBoth)
			newPathB = self._pathFrom(pathB, childofBoth)
			self._compareRecurse(newPathA, newPathB)
