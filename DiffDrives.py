import os.path
from os import path
from sys import argv
import subprocess
import os

class DiffDrives:

	#various files that don't need to be considered
	skippedFiles = [".DS_Store"]

	def __init__(self, verifiedPathA, verifiedPathB):
		self.pathA = verifiedPathA
		self.pathB = verifiedPathB
		print(f"INIT with {self.pathA} and {self.pathB}")
		print(self.captureDirectories(self.pathA))
		print(self.captureFiles(self.pathA))

	'''
	returns a list of child directories for the given path
	'''
	def captureDirectories(self, path):
		#[('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA', ['A', 'B', 'C'], ['fileA.txt', 'fileB.txt', 'fileC.txt']), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/A', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/B', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/C', [], [])]
		dirWalk = list(os.walk(path))
		childDirectories = dirWalk[0][1]
		return childDirectories
	'''
	returns a list of files in child directory for given path
	'''
	def captureFiles(self, path):
		#[('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA', ['A', 'B', 'C'], ['fileA.txt', 'fileB.txt', 'fileC.txt']), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/A', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/B', [], []), ('Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetA/C', [], [])]
		dirWalk = list(os.walk(path))
		childFiles = [f for f in dirWalk[0][2] if f not in self.skippedFiles]
		return childFiles

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
	 
