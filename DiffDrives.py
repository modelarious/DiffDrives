import os.path
from os import path
from sys import argv
import subprocess
import os

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
def compare(children):
	print("calling compare with", children)
	#('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', [], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', [], [])
	#('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', ['A'], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', [], [])
	#('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', [], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', ['A'], [])
	#('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', ['A'], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', ['A'], [])
	#('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', ['A', 'B'], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', ['A'], [])
	#('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', ['A'], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', ['A', 'B'], [])
	diffDict = dict()

	while True:
		nextA = getNext(children["A"])
		nextB = getNext(children["B"])

		#We're only looking for what's in A that isn't in B, so we don't care if children of B is None, we only worry about when we've exhausted children of A
		if nextA == None:
			print("Exhausted A, returning diff dict")
			return diffDict

		pathA, dirsA, filesA = getDetails(nextA)
		pathB, dirsB, filesB = getDetails(nextB)
		
		print(pathA, dirsA, filesA, "||", pathB, dirsB, filesB)
		print("dirs in B and in A:", [x for x in dirsB if x in dirsA])
		print("dirs in A but not in B:", [x for x in dirsA if x not in dirsB])

		union = [x for x in dirsB if x in dirsA]
		inAbutNotB = [x for x in dirsA if x not in dirsB]
		
		origPathA = "Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA"
		origPathB = "Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB"
		
		for childofBoth in union:
			children = dict({"A":getChildrenGenerator(origPathA + "/" + childofBoth), "B":getChildrenGenerator(origPathB + "/" + childofBoth)})
			print(compare(children))
		break
		

def main(pathA, pathB):
	print(f"main called with {pathA}, {pathB}")
	#verify paths exist before walking them
	if path.exists(pathA) and path.exists(pathB):
		children = dict({"A":getChildrenGenerator(pathA), "B":getChildrenGenerator(pathB)})
		#return compare(childA, childB, pathA, pathB)
		return compare(children)
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
		
		
	#else:
	#	return -1
		

if __name__ == "__main__":
	if len(argv) != 3:
		#TODO print usage
		exit(-1)

	#pass in the two paths to be diffed
	main(argv[1], argv[2])
	 
