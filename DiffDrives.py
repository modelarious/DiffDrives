import os.path
from os import path
from sys import argv

class DiffDrives:
	def __init__(self, verifiedPathA, verifiedPathB):
		self.pathA = verifiedPathA
		self.pathB = verifiedPathB
		print(f"INIT with {self.pathA} and {self.pathB}")

def main(pathA, pathB):

	#verify paths exist before creating instance of DiffDrives class
	if path.exists(pathA) and path.exists(pathB):
		instance = DiffDrives(pathA, pathB)
		

if __name__ == "__main__":
	if len(argv) != 3:
		#TODO print usage
		exit(-1)

	#pass in the two paths to be diffed
	main(argv[1], argv[2])
	 
