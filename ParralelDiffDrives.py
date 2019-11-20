from os import sep, walk
import threading
import time
import logging
import queue

LOGGING = False
if LOGGING:
	logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

queueSizeLock = threading.Lock()
queueSize = 1
ProcessingFinished = threading.Condition()
q = queue.Queue()

class ConsumerThread(threading.Thread):
	def run(self):
		global queueSize
		while True:
			if not q.empty():
				receivedPath = q.get()
				path, dirs, files = "",[],[]
				
				#Some directories won't let you enter them due to user privileges, and
				#those directories raise a StopIteration error.
				try:
					path, dirs, files = next(walk(receivedPath))
				except StopIteration:
					pass
				logging.debug('Got ' + str(path))
				
				#heavy processing here

				with queueSizeLock:
					for dir in dirs:
                    	#construct path: "path/to/current/directory" + "/" + "sub_directory"
						item = path + sep + dir 
						q.put(item)
						logging.debug('Putting ' + str(item))
                
					'''
            		We have finished with this queue entry, so we subtract 1 
            		from the queueSize.  We have also found len(dirs) new entries 
            		for the queue, so we add that to queueSize
            		'''
					queueSize += len(dirs) - 1
					
					#tell the main thread that all processing is done
					#can only happen once all dirs have been exhausted
					if queueSize == 0:
						with ProcessingFinished:
							ProcessingFinished.notify()



def queueEmpty():
	return queueSize == 0
def main():

    initialPath = '/Volumes/MyRaid'
    q.put(initialPath)
    numThreads = 350
    for consumerNum in range(1, numThreads + 1):
        c = ConsumerThread()
        c.daemon = True
        c.start()
    

    
    with ProcessingFinished:
    	ProcessingFinished.wait_for(queueEmpty)
    	return 0

main()
