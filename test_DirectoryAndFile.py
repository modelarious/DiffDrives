import pytest
from DiffDrives import main
'''
needed
each of the following cases for the top level directory:
                #('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', [], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', [], [])
                #('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', ['A'], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', [], [])
                #('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', [], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', ['A'], [])
                #('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', ['A'], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', ['A'], [])
                #('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', ['A', 'B'], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', ['A'], [])
                #('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', ['A'], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', ['A', 'B'], [])

with each of the following variations based on files
                #('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', [*], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', [*], [])
                #('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', [*], ['A']) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', [*], [])
                #('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', [*], []) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', [*], ['A'])
                #('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', [*], ['A']) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', [*], ['A'])
                #('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', [*], ['A', 'B']) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', [*], ['A'])
                #('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetA', [*], ['A']) ('Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB', [*], ['A', 'B'])


Test existing tests (like SameDirectoryStructureFlat) with each of the operands TargetA and TargetB swapped with a new set of expected outputs

test that an empty A will report that correctly and quickly

test that a large example will not mess up
'''
from TestConfigParser.YamlReader import YamlReader
from TestConfigParser.Constants import BaseDir, TargetA, TargetB
from TestConfigParser.TestCaseConfigParser import TestCaseConfigParser
from os import sep

parsedYaml = YamlReader().fetchYaml("configTesting.yml")
x = TestCaseConfigParser(parsedYaml)

@pytest.mark.parametrize("directory, expected_output, testcase_num", x.getTestCases())
def test_eval(directory, expected_output, testcase_num):
	basePath = BaseDir + sep + directory
	print(basePath, expected_output, testcase_num)
	result = main(basePath + sep + TargetA, basePath + sep + TargetB)
	assert (result == expected_output)
