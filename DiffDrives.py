from pprint import pprint
from os import path
from sys import argv
from Factories.CompareTwoDirectoriesEngineFactory import CompareTwoDirectoriesEngineFactory
from Factories.CopyFilesAndDirectoriesEngineFactory import CopyFilesAndDirectoriesEngineFactory
from Logging import printSTATUS

def main(pathA, pathB):
	printSTATUS(f"main called with {pathA}, {pathB}")
	twoDirComp = CompareTwoDirectoriesEngineFactory.getEngine()
	copyContents = CopyFilesAndDirectoriesEngineFactory.getEngine()

	#verify paths exist before walking them
	if path.exists(pathA) and path.exists(pathB):
		contentsInAButNotB = twoDirComp.compare(pathA, pathB)
		pprint(contentsInAButNotB, width=300)
		# userConfirmation = input(f"Would you like to copy all the above files and directories over from {pathA} to {pathB} (y/n): ")
		# if userConfirmation.lower() == "y":
		# 	print("COPYING")
		copyContents.copyFilesAndDirectories(pathA, pathB, contentsInAButNotB)
		return contentsInAButNotB.getDiff()	
	return -1

if __name__ == "__main__":
	if len(argv) != 3:
		print("usage: python3 DiffDrives.py /path/to/dir/1 /path/to/dir/2")
		exit(-1)

	#pass in the two paths to be diffed
	returnCode = main(argv[1], argv[2])
	exit(returnCode)
	 
