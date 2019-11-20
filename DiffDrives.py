''' 
adapted from https://www.bogotobogo.com/python/Multithread/python_multithreading_Synchronization_Producer_Consumer_using_Queue.php
fetched November 20, 2019
'''
import pprint
from os import path, sep, walk
from sys import argv
import threading

import time
import logging
import queue

'''
DEBUG, THREADINGDEBUG and STATUS are for debug purposes and just change the level of logging that is occuring.
These don't ever need to be used unless you want more detail into what is going on
'''
DEBUG = False
def printif(*args):
	if DEBUG == True:
		print(args)

THREADINGDEBUG = True
if THREADINGDEBUG == True:
	logging.basicConfig(level=logging.DEBUG,
			format='(%(threadName)-9s) %(message)s',)

STATUS = False
def printSTATUS(*args):
	if STATUS == True:
		print(args)

#various files that don't need to be considered
skippedFiles = [".DS_Store"]

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
- getDirs() returns all subdirectories in the current directory
- getFiles() returns all files in the current directory with the exclusion of anything in "skippedFiles"
'''
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


'''
Walks through the directory structure and generates tuples of three entries 
that represents where we are in the file system:
(
	'/path/to/directory', 
	['dirs', 'in', 'this', 'directory'], 
	['files.txt', 'in.txt', 'this.txt', 'directory.txt']
)
'''
def getChildrenGenerator(path):
	return walk(path)

#wrapper to catch the StopIteration error
def getNext(generator):
	try:
		return next(generator)
	except StopIteration:
		return None
'''
[('Testing/DifferentDirectoryStructureDifferentFilesFlat', ['DiffTargetA', 'DiffTargetB'], [".DS_Store"]), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA', ['A', 'B', 'C'], ['fileA.txt', 'fileB.txt', 'fileC.txt']), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/A', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/B', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/C', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB', ['A', 'B'], ['fileA.txt', 'fileB.txt']), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB/A', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB/B', [], [])]
'''

def compare(childA, childB, pathA, pathB):
	diffSolu = {"files":[], "dirs":[]}
	def _compare_recurse(childA, childB, pathA, pathB):
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
		
		#print(nextA, nextB)

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
		dirExtension = [pathB + sep + x for x in inAbutNotB]
		fileExtension = [pathB + sep + x for x in filesInAbutNotInB] 
		printSTATUS("extending the solution by", dirExtension)
		printSTATUS("extending the solution by", fileExtension)
		diffSolu["dirs"].extend(dirExtension)
		diffSolu["files"].extend(fileExtension)
		

		for childofBoth in union:
			newPathA = pathA + sep + childofBoth
			newPathB = pathB + sep + childofBoth
			_compare_recurse(getChildrenGenerator(newPathA), getChildrenGenerator(newPathB), newPathA, newPathB)

	_compare_recurse(childA, childB, pathA, pathB)
	return diffSolu

q = queue.Queue()
class ConsumerThread(threading.Thread):
	def __init__(self, group=None, target=None, name=None,
			args=(), kwargs=None, verbose=None):
		super(ConsumerThread,self).__init__()
		self.name = name
		return

	def run(self):
		while True:
			if not q.empty():
				item = q.get()
				childA = getChildrenGenerator(item)
				nextA = getNext(childA)
				path,dirs,files = getDetails(nextA)
				logging.debug('Getting ' + str(item) 
						+ ' : ' + str(q.qsize()) + ' items in queue')
				for dir in dirs:
					item = path + sep + dir
					q.put(item)
					logging.debug('Putting ' + str(item)
						+ ' : ' + str(q.qsize()) + ' items in queue')
		return


def main(pathA, pathB):
	numThreads = 20
	for consumerNum in range(1, numThreads + 1):
		ConsumerThread(name='consumer' + str(consumerNum)).start()
	item = 'Testing'
	item = '/Volumes/MyRAID'
	q.put(item)
	time.sleep(40)
	return
	printSTATUS(f"main called with {pathA}, {pathB}")

	#verify paths exist before walking them
	if path.exists(pathA) and path.exists(pathB):
		diffSolu = compare(getChildrenGenerator(pathA), getChildrenGenerator(pathB), pathA, pathB)
		print("final solution = '", diffSolu, "'")
		pprint.pprint(diffSolu, width=300)
		return diffSolu


		#('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA', ['A', 'B', 'C'], ['fileA.txt', 'fileB.txt', 'fileC.txt']), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/A', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/B', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/C', [], [])
		#('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB', ['A', 'B'], ['fileA.txt', 'fileB.txt']), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB/A', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB/B', [], [])
		
		
	#else:
	#	return -1
		

if __name__ == "__main__":
	if len(argv) != 3:
		#TODO print usage
		print("usage: python3 DiffDrives.py /path/to/dir/1 /path/to/dir/2")
		exit(-1)

	#pass in the two paths to be diffed
	main(argv[1], argv[2])
	 
