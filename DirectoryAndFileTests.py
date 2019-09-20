import pytest
from DiffDrives import main

BaseDir = "Testing/"
TargetA = "DiffTargetA"
TargetB = "DiffTargetB"

Directories = ['SameDirectoryStructureFlat', 'SameDirectoryStructureNested', 'DifferentDirectoryStructureFlat', 'DifferentDirectoryStructureNested', 'SameFilesFlat', 'SameFilesNested', 'DifferentFilesFlat', 'DifferentFilesNested', 'DifferentDirectoryStructureDifferentFilesFlat', 'DifferentDirectoryStructureDifferentFilesNested']

ExpectedOutputs = ["Hello World"] * len(Directories)
TestCaseNums = ["JUJU"] * len(Directories)


@pytest.mark.parametrize("directory, expected_output, testcase_num", list(zip(Directories, ExpectedOutputs, TestCaseNums)))
def test_eval(directory, expected_output, testcase_num):
	print(BaseDir + directory, expected_output, testcase_num)
	main(BaseDir + directory + "/" + TargetA, BaseDir + directory + "/" + TargetB)
	#assert directory == expected_output
