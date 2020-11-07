from pprint import pprint
from os import path, sep, walk
from sys import argv

'''
DEBUG and STATUS are for debug purposes and just change the level of logging that is occuring.
These don't ever need to be used unless you want more detail into what is going on
'''
DEBUG = False
def printif(*args):
	if DEBUG == True:
		print(args)

STATUS = False
def printSTATUS(*args):
	if STATUS == True:
		print(args)


'''
When using os.walk we get a tuple of three entries that represents 
where we are in the file system:
(
    '/path/to/directory', 
    ['dirs', 'in', 'this', 'directory'], 
    ['files.txt', 'in.txt', 'this.txt', 'directory.txt']
)

getDetails() unpacks that structure with special functions:
- getPath() returns the path of the current directory
- getDirs() returns a set of all subdirectories in the current directory
- getFiles() returns a set of all files in the current directory with the exclusion of anything in "skippedFiles"
'''
class DirectoryInfo(object):
    def __init__(self, nameDirsFilesTuple):
        #various files that don't need to be considered
        skippedFiles = [".DS_Store"]

        self.path = nameDirsFilesTuple[0]
        self.containedDirectories = set(nameDirsFilesTuple[1])
        self.containedFiles = set((f for f in nameDirsFilesTuple[2] if f not in skippedFiles))

    def getPath(self):
        return self.path

    def getDirs(self):
        return self.containedDirectories

    def getFiles(self):
        return self.containedFiles


'''
Walks through the directory structure and generates tuples of three entries 
that represents where we are in the file system:
(
	'/path/to/directory', 
	['dirs', 'in', 'this', 'directory'], 
	['files.txt', 'in.txt', 'this.txt', 'directory.txt']
)
'''
def getChild(path):
	try:
		return DirectoryInfo(next(walk(path)))
	except StopIteration:
		return None
    
'''
[('Testing/DifferentDirectoryStructureDifferentFilesFlat', ['DiffTargetA', 'DiffTargetB'], [".DS_Store"]), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA', ['A', 'B', 'C'], ['fileA.txt', 'fileB.txt', 'fileC.txt']), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/A', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/B', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/C', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB', ['A', 'B'], ['fileA.txt', 'fileB.txt']), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB/A', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB/B', [], [])]
'''

def compare(pathA, pathB):
	diffSolu = {"files":[], "dirs":[]}
	def _compare_recurse(childA, childB, pathA, pathB):
		printSTATUS("calling compare with", pathA, pathB)
		#('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', [], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', [], [])
		#('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', ['A'], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', [], [])
		#('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', [], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', ['A'], [])
		#('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', ['A'], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', ['A'], [])
		#('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', ['A', 'B'], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', ['A'], [])
		#('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', ['A'], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', ['A', 'B'], [])
		
		#print(childA, childB)

		#We're only looking for what's in A that isn't in B, so we don't care if children of B is None, we only worry about when we've exhausted children of A
		if childA == None:
			printif("Exhausted A, returning diff dict")
			return None

		pathA, dirsA, filesA = childA.getPath(), childA.getDirs(), childA.getFiles()
		pathB, dirsB, filesB = childB.getPath(), childB.getDirs(), childB.getFiles()
        
		union = [x for x in dirsB if x in dirsA]
		inAbutNotB = [x for x in dirsA if x not in dirsB]
		filesInAbutNotInB = [x for x in filesA if x not in filesB]

		printif(pathA, dirsA, filesA, "||", pathB, dirsB, filesB)
		printSTATUS("dirs in B and in A:", union)
		printSTATUS("dirs in A but not in B:", inAbutNotB)

		#add the path to everything in "inAbutNotB" and track it
		dirExtension = [pathB + sep + x for x in inAbutNotB]
		fileExtension = [pathB + sep + x for x in filesInAbutNotInB] 
		printSTATUS("extending the solution by", dirExtension)
		printSTATUS("extending the solution by", fileExtension)
		diffSolu["dirs"].extend(dirExtension)
		diffSolu["files"].extend(fileExtension)
		

		for childofBoth in union:
			newPathA = pathA + sep + childofBoth
			newPathB = pathB + sep + childofBoth
			_compare_recurse(getChild(newPathA), getChild(newPathB), newPathA, newPathB)

	_compare_recurse(getChild(pathA), getChild(pathB), pathA, pathB)
	return diffSolu

def main(pathA, pathB):
	printSTATUS(f"main called with {pathA}, {pathB}")

	#verify paths exist before walking them
	if path.exists(pathA) and path.exists(pathB):
		diffSolu = compare(pathA, pathB)
		pprint(diffSolu, width=300)
		return diffSolu


		#('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA', ['A', 'B', 'C'], ['fileA.txt', 'fileB.txt', 'fileC.txt']), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/A', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/B', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/C', [], [])
		#('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB', ['A', 'B'], ['fileA.txt', 'fileB.txt']), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB/A', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB/B', [], [])
		
		
	else:
		return -1
		

if __name__ == "__main__":
	if len(argv) != 3:
		print("usage: python3 DiffDrives.py /path/to/dir/1 /path/to/dir/2")
		exit(-1)

	#pass in the two paths to be diffed
	main(argv[1], argv[2])
	 
