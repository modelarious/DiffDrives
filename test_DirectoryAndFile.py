import pytest
from DiffDrives import main
'''
needed

Test existing tests (like SameDirectoryStructureFlat) with each of the operands targetA and targetB swapped with a new set of expected outputs

test that an empty A will report that correctly and quickly

test that a large example will not mess up
'''
from TestConfigParser.YamlReader import YamlReader
from TestConfigParser.Constants import baseDir, targetA, targetB
from TestConfigParser.TestCaseConfigParser import TestCaseConfigParser
from os import sep

parsedYaml = YamlReader().fetchYaml("configTesting.yml")
testCaseConfigParser = TestCaseConfigParser(parsedYaml)

@pytest.mark.parametrize("directory, expected_output, testcase_num", testCaseConfigParser.getTestCases())
def test_eval(directory, expected_output, testcase_num):
	basePath = baseDir + sep + directory
	print(basePath, expected_output, testcase_num)
	result = main(basePath + sep + targetA, basePath + sep + targetB)
	assert(result == expected_output)
