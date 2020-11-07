from pprint import pprint
from os import path
from sys import argv
from DiffDrives.Factories.CompareTwoDirectoriesEngineFactory import CompareTwoDirectoriesEngineFactory
from DiffDrives.Logging import printSTATUS

def main(pathA, pathB):
	printSTATUS(f"main called with {pathA}, {pathB}")
	twoDirComp = CompareTwoDirectoriesEngineFactory.getEngine()

	#verify paths exist before walking them
	if path.exists(pathA) and path.exists(pathB):
		diffSolution = twoDirComp.compare(pathA, pathB)
		pprint(diffSolution, width=300)
		return diffSolution	
	return -1

if __name__ == "__main__":
	if len(argv) != 3:
		print("usage: python3 DiffDrives.py /path/to/dir/1 /path/to/dir/2")
		exit(-1)

	#pass in the two paths to be diffed
	returnCode = main(argv[1], argv[2])
	exit(returnCode)
	 
