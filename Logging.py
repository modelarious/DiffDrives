'''
DEBUG and STATUS are for debug purposes and just change the level of logging that is occuring.
These don't ever need to be used unless you want more detail into what is going on
'''
DEBUG = False
def printDEBUG(*args):
	if DEBUG == True:
		print(*args)

STATUS = False
def printSTATUS(*args):
	if STATUS == True:
		print(*args)
