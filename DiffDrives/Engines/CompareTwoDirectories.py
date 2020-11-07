from os import sep
from DiffDrives.DataStructures.DiffDataStructure import DiffDataStructure
from DiffDrives.Logging import printSTATUS, printDEBUG

'''
[('Testing/DifferentDirectoryStructureDifferentFilesFlat', ['DiffTargetA', 'DiffTargetB'], [".DS_Store"]), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA', ['A', 'B', 'C'], ['fileA.txt', 'fileB.txt', 'fileC.txt']), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/A', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/B', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/C', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB', ['A', 'B'], ['fileA.txt', 'fileB.txt']), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB/A', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB/B', [], [])]
'''
class CompareTwoDirectories(object):
	def __init__(self, directoryInfoFetcher):
		self.directoryInfoFetcher = directoryInfoFetcher

	def compare(self, pathA, pathB):
		self.dataStorage = DiffDataStructure()
		self._compareRecurse(pathA, pathB)
		return self.dataStorage.getDiff()

	def _getResultsOfSetOperations(self, dirsA, dirsB, filesA, filesB):
		partialUnion = [x for x in dirsB if x in dirsA]
		printSTATUS("dirs in B that are also in A:", partialUnion)

		dirsInAbutNotB = [x for x in dirsA if x not in dirsB]
		printSTATUS("dirs in A but not in B:", dirsInAbutNotB)

		filesInAbutNotInB = [x for x in filesA if x not in filesB]
		printSTATUS("files in A but not in B:", filesInAbutNotInB)

		return partialUnion, dirsInAbutNotB, filesInAbutNotInB
	
	def _trackDifferencesAndCalculateNextCandidates(self, directoryInfoA, directoryInfoB):
		pathA, dirsA, filesA = directoryInfoA.getPath(), directoryInfoA.getDirs(), directoryInfoA.getFiles()
		pathB, dirsB, filesB = directoryInfoB.getPath(), directoryInfoB.getDirs(), directoryInfoB.getFiles()
		printDEBUG(pathA, dirsA, filesA, "||", pathB, dirsB, filesB)

		partialUnion, dirsInAbutNotB, filesInAbutNotInB = self._getResultsOfSetOperations(dirsA, dirsB, filesA, filesB)

		#add the path to everything in "dirsInAbutNotB" and track it
		dirExtension = [pathB + sep + x for x in dirsInAbutNotB]
		fileExtension = [pathB + sep + x for x in filesInAbutNotInB] 

		self.dataStorage.trackDirs(dirExtension)
		self.dataStorage.trackFiles(fileExtension)

		return partialUnion

	def _compareRecurse(self, pathA, pathB):
		printSTATUS("calling compareRecurse with", pathA, pathB)

		directoryInfoA = self.directoryInfoFetcher.getDirectoryInfo(pathA)
		directoryInfoB = self.directoryInfoFetcher.getDirectoryInfo(pathB)

		#We're only looking for what's in A that isn't in B, so we don't care if children of B is None, we only worry about when we've exhausted children of A
		if directoryInfoA == None:
			printDEBUG("Exhausted A, returning diff dict")
			return None

		partialUnion = self._trackDifferencesAndCalculateNextCandidates(directoryInfoA, directoryInfoB)
		
		for childofBoth in partialUnion:
			newPathA = pathA + sep + childofBoth
			newPathB = pathB + sep + childofBoth
			self._compareRecurse(newPathA, newPathB)
