import pytest
from DiffDrives import main
'''
XXX needed
Test existing tests (like SameDirectoryStructureFlat) with each of the operands targetA and targetB swapped with a new set of expected outputs
'''
from TestConfigParser.YamlReader import YamlReader
from TestConfigParser.Constants import baseDir, targetA, targetB
from TestConfigParser.TestCaseConfigParser import TestCaseConfigParser
from Factories.CompareTwoDirectoriesEngineFactory import CompareTwoDirectoriesEngineFactory
from Factories.CopyFilesAndDirectoriesEngineFactory import CopyFilesAndDirectoriesEngineFactory
from DataStructures.DiffDataStructure import DiffDataStructure
from os import path
	
parsedYaml = YamlReader().fetchYaml("configTesting.yml")
testCaseConfigParser = TestCaseConfigParser(parsedYaml)

@pytest.mark.parametrize("directory, expected_output, testcase_num", testCaseConfigParser.getTestCases())
def test_compare(directory, expected_output, testcase_num):
	basePath = path.join(baseDir, directory)
	pathA = path.join(basePath, targetA)
	pathB = path.join(basePath, targetB)
	print(basePath, expected_output, testcase_num)

	twoDirComp = CompareTwoDirectoriesEngineFactory.getEngine()
	contentsInAButNotB = twoDirComp.compare(pathA, pathB)

	assert(contentsInAButNotB.getDiff() == expected_output)

@pytest.mark.parametrize("directory, expected_output, testcase_num", testCaseConfigParser.getTestCases())
def test_copy(directory, expected_output, testcase_num):
	basePath = path.join(baseDir, directory)
	pathA = path.join(basePath, targetA)
	pathB = path.join(basePath, targetB)
	print(basePath, expected_output, testcase_num)

	twoDirComp = CompareTwoDirectoriesEngineFactory.getEngine()
	contentsInAButNotB = twoDirComp.compare(pathA, pathB)

	copyContents = CopyFilesAndDirectoriesEngineFactory.getEngine()
	copyContents.copyFilesAndDirectories(pathA, pathB, contentsInAButNotB)

	twoDirComp_afterCopy = CompareTwoDirectoriesEngineFactory.getEngine()
	contentsInAButNotB_afterCopy = twoDirComp.compare(pathA, pathB)

	emptyDiff = DiffDataStructure()

	assert(contentsInAButNotB_afterCopy.getDiff() == emptyDiff.getDiff())
