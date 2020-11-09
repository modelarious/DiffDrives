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
# XXX make these shared constants imported from the TestConfigParser
from os import sep
BaseDir = "Testing" + sep
TargetA = "DiffTargetA"
TargetB = "DiffTargetB"

class TestCaseConfigParser(object):
	def __init__(self, parsedYaml):
		self.parsedYaml = parsedYaml
		self.testCaseStorage = []
		self.tcNum = 1
		self._collectTestCases()
	
	def getTestCases(self):
		return self.testCaseStorage
	
	def _collectTestCases(self):
		for testCaseName in self.parsedYaml.keys():
			self._trackTestCase(testCaseName, self.parsedYaml[testCaseName]['expectedOutput'])

	def _trackTestCase(self, testCaseName, expectedOutput):
		expectedOutputAdjusted = self._addExtendedPathInfo(testCaseName, expectedOutput)
		self.testCaseStorage.append(
			(
				testCaseName,
				expectedOutputAdjusted,
				self.tcNum
			)
		)

		self.tcNum += 1

	def _addExtendedPathInfo(self, testCaseName, expectedOutput):
		# add the base test dir and the testCaseName dir to the front of every file and directory in expected results
		expectedOutputAdjusted = dict()
		for k, v in expectedOutput.items():
			newV = []
			for entry in v:
				newV.append(BaseDir + testCaseName + sep + entry)
			expectedOutputAdjusted[k] = sorted(newV)
		return expectedOutputAdjusted



from TestConfigParser.YamlReader import YamlReader
parsedYaml = YamlReader().fetchYaml("configTesting.yml")
x = TestCaseConfigParser(parsedYaml)
print(x.getTestCases())


Directories = ['SameDirectoryStructureFlat', 'SameDirectoryStructureNested', 'DifferentDirectoryStructureFlat', 'DifferentDirectoryStructureNested', 'SameFilesFlat', 'SameFilesNested', 'DifferentFilesFlat', 'DifferentFilesNested', 'DifferentDirectoryStructureDifferentFilesFlat', 'DifferentDirectoryStructureDifferentFilesNested']

ExpectedOutputs = [
	{'dirs': [], 'files': []}, 
	{'dirs': [], 'files': []},
	{'dirs': ['Testing/DifferentDirectoryStructureFlat/DiffTargetB/C'], 'files': []},
	{'dirs': ['Testing/DifferentDirectoryStructureNested/DiffTargetB/A/F'], 'files': []},
	{'dirs': [], 'files': []},
	{'dirs': [], 'files': []},
	{'dirs': [], 'files': ['Testing/DifferentFilesFlat/DiffTargetB/fileC.txt']},
	{'dirs': [], 'files': ['Testing/DifferentFilesNested/DiffTargetB/A/E/fileC.txt']},
	{'dirs': ['Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB/C'], 'files': ['Testing/DifferentDirectoryStructureDifferentFilesFlat/DiffTargetB/fileC.txt']},
	{'dirs': ['Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB/A/F'], 'files': ['Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB/A/E/fileC.txt']}]

	
TestCaseNums = [f"TC_{i+1:03d}" for i in range(len(Directories))]


@pytest.mark.parametrize("directory, expected_output, testcase_num", x.getTestCases())
def test_eval(directory, expected_output, testcase_num):
	print(BaseDir + directory, expected_output, testcase_num)
	result = main(BaseDir + directory + "/" + TargetA, BaseDir + directory + "/" + TargetB)
	assert ( result == expected_output)


