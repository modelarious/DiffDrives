import os.path
from os import path
from sys import argv
import subprocess
import os

DEBUG = False
def printif(*args):
	if DEBUG == True:
		print(args)

STATUS = False
def printSTATUS(*args):
	if STATUS == True:
		print(args)

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

def compareWrapper(childA, childB, pathA, pathB):
	diffSolu = {"files":[], "dirs":[]}
	def compare(childA, childB, pathA, pathB):
		printSTATUS("calling compare with", pathA, pathB)
		#('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', [], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', [], [])
		#('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', ['A'], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', [], [])
		#('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', [], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', ['A'], [])
		#('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', ['A'], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', ['A'], [])
		#('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', ['A', 'B'], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', ['A'], [])
		#('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', ['A'], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', ['A', 'B'], [])

		#XXX XXX XXX generators are not needed anymore, you only need the first value from the generator
		nextA = getNext(childA)
		nextB = getNext(childB)

		#We're only looking for what's in A that isn't in B, so we don't care if children of B is None, we only worry about when we've exhausted children of A
		if nextA == None:
			printif("Exhausted A, returning diff dict")
			return None

		pathA, dirsA, filesA = getDetails(nextA)
		pathB, dirsB, filesB = getDetails(nextB)
		union = [x for x in dirsB if x in dirsA]
		inAbutNotB = [x for x in dirsA if x not in dirsB]
		filesInAbutNotInB = [x for x in filesA if x not in filesB]

		printif(pathA, dirsA, filesA, "||", pathB, dirsB, filesB)
		printSTATUS("dirs in B and in A:", union)
		printSTATUS("dirs in A but not in B:", inAbutNotB)

		#add the path to everything in "inAbutNotB" and track it
		dirExtension = [pathB + os.sep + x for x in inAbutNotB]
		fileExtension = [pathB + os.sep + x for x in filesInAbutNotInB] 
		printSTATUS("extending the solution by", dirExtension)
		printSTATUS("extending the solution by", fileExtension)
		diffSolu["dirs"].extend(dirExtension)
		diffSolu["files"].extend(fileExtension)
		

		for childofBoth in union:
			newPathA = pathA + os.sep + childofBoth
			newPathB = pathB + os.sep + childofBoth
			compare(getChildrenGenerator(newPathA), getChildrenGenerator(newPathB), newPathA, newPathB)

	compare(childA, childB, pathA, pathB)
	return diffSolu

def main(pathA, pathB):
	printSTATUS(f"main called with {pathA}, {pathB}")

	#verify paths exist before walking them
	if path.exists(pathA) and path.exists(pathB):
		diffSolu = compareWrapper(getChildrenGenerator(pathA), getChildrenGenerator(pathB), pathA, pathB)
		print("final solution = '", diffSolu, "'")
		return diffSolu


		#('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA', ['A', 'B', 'C'], ['fileA.txt', 'fileB.txt', 'fileC.txt']), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/A', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/B', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/C', [], [])
		#('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB', ['A', 'B'], ['fileA.txt', 'fileB.txt']), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB/A', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB/B', [], [])
		
		
	#else:
	#	return -1
		

if __name__ == "__main__":
	if len(argv) != 3:
		#TODO print usage
		exit(-1)

	#pass in the two paths to be diffed
	main(argv[1], argv[2])
	 
