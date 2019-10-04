import os.path
from os import path
from sys import argv
import subprocess
import os


'''
[('Testing/DifferentDirectoryStructureDifferentFilesFlat', ['DiffTargetA', 'DiffTargetB'], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA', ['A', 'B', 'C'], ['fileA.txt', 'fileB.txt', 'fileC.txt']), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/A', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/B', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/C', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB', ['A', 'B'], ['fileA.txt', 'fileB.txt']), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB/A', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB/B', [], [])]
'''
class DiffDrives:

	#various files that don't need to be considered
	skippedFiles = [".DS_Store"]

	def __init__(self, verifiedPathA, verifiedPathB):
		self.pathA = verifiedPathA
		self.pathB = verifiedPathB
		print(f"INIT with {self.pathA} and {self.pathB}")
		print(self._captureChild(self.pathA))

	def _captureChild(self, path):
		return self._captureDirectories(path), self._captureFiles(path)

	'''
	returns a list of child directories for the given path
	'''
	def _captureDirectories(self, path):
		#[('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA', ['A', 'B', 'C'], ['fileA.txt', 'fileB.txt', 'fileC.txt']), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/A', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/B', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/C', [], [])]
		dirWalk = list(os.walk(path))
		childDirectories = dirWalk[0][1]
		return childDirectories
	'''
	returns a list of files in child directory for given path
	'''
	def _captureFiles(self, path):
		#[('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA', ['A', 'B', 'C'], ['fileA.txt', 'fileB.txt', 'fileC.txt']), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/A', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/B', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/C', [], [])]
		dirWalk = list(os.walk(path))
		childFiles = [f for f in dirWalk[0][2] if f not in self.skippedFiles]
		return childFiles

	'''
	run methods that will process two directories
	'''
	def processDiff(self):
		return self._captureChild(self.pathA), self._captureChild(self.pathB)















#various files that don't need to be considered
skippedFiles = [".DS_Store"]

def getDirs(nameDirsFilesTuple):
	return nameDirsFilesTuple[1]

def getFiles(nameDirsFilesTuple):
	return [f for f in nameDirsFilesTuple[2] if f not in skippedFiles]

def getChildren(path):
	return list(os.walk(path))
'''
[('Testing/DifferentDirectoryStructureDifferentFilesFlat', ['DiffTargetA', 'DiffTargetB'], [".DS_Store"]), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA', ['A', 'B', 'C'], ['fileA.txt', 'fileB.txt', 'fileC.txt']), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/A', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/B', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/C', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB', ['A', 'B'], ['fileA.txt', 'fileB.txt']), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB/A', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB/B', [], [])]
'''
def main(pathA, pathB):

	#verify paths exist before walking them
	if path.exists(pathA) and path.exists(pathB):
		children = dict({"A":getChildren(pathA), "B":getChildren(pathB)})

		pointer = 0
		maxSizeOfChilren = max(map(len, children.values()))
		while pointer < maxSizeOfChilren:
			dirs = dict({k:getDirs(v[0]) for k,v in children.items()})	
			print(dirs)
			pointer += 1

		#('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA', ['A', 'B', 'C'], ['fileA.txt', 'fileB.txt', 'fileC.txt']), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/A', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/B', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/C', [], [])
		#('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB', ['A', 'B'], ['fileA.txt', 'fileB.txt']), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB/A', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB/B', [], [])
		
		
	else:
		return -1
		

if __name__ == "__main__":
	if len(argv) != 3:
		#TODO print usage
		exit(-1)

	#pass in the two paths to be diffed
	main(argv[1], argv[2])
	 
