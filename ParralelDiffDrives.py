from os import sep, walk
import threading
import time
import logging
import queue
import pprint

'''
DEBUG, STATUS and LOGGING are for debug purposes and just change the level of logging that is occuring.
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
		
LOGGING = False
if LOGGING:
	logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

hasBeenInit = False #if this file has been initialized already, then don't make more threads
queueSizeLock = threading.Lock()
queueSize = 1
ProcessingFinished = threading.Condition()
q = queue.Queue()
diffSolu = {"files":[], "dirs":[]}

class ConsumerThread(threading.Thread):

	skippedFiles = [".DS_Store"]

	def _getDirInfo(self, receivedPath):
		path, dirs, files = "",[],[]
		
		#Some directories won't let you enter them due to user privileges, and
		#those directories raise a StopIteration error.
		try:
			path, dirs, files = next(walk(receivedPath))
			files = [f for f in files if f not in self.skippedFiles]
		except StopIteration:
			pass
		return path, dirs, files
		
	def run(self):
		global queueSize
		while True:
			if not q.empty():
				receivedPathA, receivedPathB  = q.get()
				printif(receivedPathA, receivedPathB)
				
				pathA, dirsA, filesA = self._getDirInfo(receivedPathA)
				pathB, dirsB, filesB = self._getDirInfo(receivedPathB)
				'''
				printif(self._getDirInfo(receivedPathA))
				printif(self._getDirInfo(receivedPathB))
				
				logging.debug('Got ' + str(pathA) + str(pathB))
				'''
				#heavy processing here
				union = [x for x in dirsB if x in dirsA]
				inAbutNotB = [x for x in dirsA if x not in dirsB]
				filesInAbutNotInB = [x for x in filesA if x not in filesB]
				'''
				printif(pathA, dirsA, filesA, "||", pathB, dirsB, filesB)
				printSTATUS("dirs in B and in A:", union)
				printSTATUS("dirs in A but not in B:", inAbutNotB)
				'''
				#add the path to everything in "inAbutNotB" and track it
				dirExtension = [pathB + sep + x for x in inAbutNotB] #XXX this should be pathA and so should the one below
				fileExtension = [pathB + sep + x for x in filesInAbutNotInB] 
				'''
				printSTATUS("extending the dir solution by", dirExtension)
				printSTATUS("extending the file solution by", fileExtension)
				'''
				diffSolu["dirs"].extend(dirExtension)
				diffSolu["files"].extend(fileExtension)
				
				'''
				if dirExtension != []:
					print("extending the dir solution by", dirExtension, "as I received", pathA, dirsA, filesA, "||", pathB, dirsB, filesB)
				if fileExtension != []:
					print("extending the file solution by", fileExtension, "as I received", pathA, dirsA, filesA, "||", pathB, dirsB, filesB)
				'''

				with queueSizeLock:
					#printif("Putting in", union)
					for childOfBoth in union:
                    	#construct path: "path/to/current/directory" + "/" + "sub_directory"
						item = (pathA + sep + childOfBoth, pathB + sep + childOfBoth) 
						q.put(item)
						#logging.debug('Putting ' + str(item))
                	
					'''
            		We have finished with this queue entry, so we subtract 1 
            		from the queueSize.  We have also found len(union) new entries 
            		for the queue, so we add that to queueSize
            		'''
					logging.debug('initial queue size ' + str(queueSize))
					queueSize += len(union) - 1
					logging.debug('after queue size ' + str(queueSize))
					
					#tell the main thread that all processing is done
					#can only happen once all dirs have been exhausted
					if queueSize == 0:
						with ProcessingFinished:
							print("notifying main thread")
							ProcessingFinished.notify()



def queueEmpty():
	return queueSize == 0
	
def main(initialPathA, initialPathB, numThreads = 350):
	global queueSize, hasBeenInit, diffSolu

	#initialize threads the first time
	if hasBeenInit != True:
		hasBeenInit = True
		for consumerNum in range(1, numThreads + 1):
			c = ConsumerThread()
			c.daemon = True
			c.start()
	
	#reset globals
	queueSize = 1
	diffSolu = {"files":[], "dirs":[]}
	
	#add first path to the queue. Processing will fill up diffSolu
	initialPath = (initialPathA, initialPathB)
	q.put(initialPath)
    
	#main thread waits for all processing to be done, then kills the program
	with ProcessingFinished:
		ProcessingFinished.wait_for(queueEmpty)
		pprint.pprint(diffSolu, width=300)
		return diffSolu
