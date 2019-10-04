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

def getDetails(nameDirsFilesTuple):
	tup = nameDirsFilesTuple
	if tup == None:
		return None, None, None
	return getPath(tup), getDirs(tup), getFiles(tup)

def getPath(nameDirsFilesTuple):
	return nameDirsFilesTuple[0]

def getDirs(nameDirsFilesTuple):
	return nameDirsFilesTuple[1]

def getFiles(nameDirsFilesTuple):
	return [f for f in nameDirsFilesTuple[2] if f not in skippedFiles]


def getChildrenGenerator(path):
	return os.walk(path)

def getNext(generator):
	try:
		return next(generator)
	except StopIteration:
		return None
'''
[('Testing/DifferentDirectoryStructureDifferentFilesFlat', ['DiffTargetA', 'DiffTargetB'], [".DS_Store"]), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA', ['A', 'B', 'C'], ['fileA.txt', 'fileB.txt', 'fileC.txt']), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/A', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/B', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/C', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB', ['A', 'B'], ['fileA.txt', 'fileB.txt']), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB/A', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB/B', [], [])]
'''
def main(pathA, pathB):
	print(f"main called with {pathA}, {pathB}")
	#verify paths exist before walking them
	if path.exists(pathA) and path.exists(pathB):
		children = dict({"A":getChildrenGenerator(pathA), "B":getChildrenGenerator(pathB)})
		
		#root directory, needs a special case
		#FirstA = getNext(children["A"])
		#FirstB = getNext(children["B"])
		
		#if children of A don't exist, return
		#We're only looking for what's in A that isn't in B, so we don't care if children of B is None, we only worry about when we've exhausted children of A
		#if FirstA == None:
		#	return

		#Case: both directory lists empty
		#compare files
		#('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', [], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', [], [])

		#Case: TargetA has a directory, TargetB has none
		#Include TargetA's directory in the results
		#compare files
		#('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', ['A'], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', [], [])    
		#('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', [], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', ['A'], [])    
		#('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', ['A'], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', ['A'], [])
		#('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', ['A', 'B'], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', ['A'], [])
		#('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', ['A'], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', ['A', 'B'], [])
		while True:
			nextA = getNext(children["A"])
			nextB = getNext(children["B"])
			
			#We're only looking for what's in A that isn't in B, so we don't care if children of B is None, we only worry about when we've exhausted children of A
			if nextA == None:
				return

			pathA, dirsA, filesA = getDetails(nextA)
			nextA = getDetails(nextA)
			nextB = getDetails(nextB)

			print(nextA, nextB)

		'''
		pointer = 0
		maxSizeOfChilren = max(map(len, children.values()))
		while pointer < maxSizeOfChilren:
			dirs = dict({k:getDirs(v[0]) for k,v in children.items()})	
			print(dirs)
			pointer += 1
		'''
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
	 
