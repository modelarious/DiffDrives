import pytest
import ParralelDiffDrives
import DiffDrives
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


Test existing tests (like SameDirectoryStructureFlat) with each of the operands targetA and targetB swapped with a new set of expected outputs

test that an empty A will report that correctly and quickly

test that a large example will not mess up
'''
baseDir = "Testing/"
targetA = "DiffTargetA"
targetB = "DiffTargetB"

Directories = [
	'SameDirectoryStructureFlat', 
	'SameDirectoryStructureNested', 
	'DifferentDirectoryStructureFlat', 
	'DifferentDirectoryStructureNested', 
	'SameFilesFlat', 
	'SameFilesNested', 
	'DifferentFilesFlat', 
	'DifferentFilesNested', 
	'DifferentDirectoryStructureDifferentFilesFlat', 
	'DifferentDirectoryStructureDifferentFilesNested'
]

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
	{'dirs': ['Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB/A/F'], 'files': ['Testing/DifferentDirectoryStructureDifferentFilesNested/DiffTargetB/A/E/fileC.txt']}
]
	
TestCaseNums = [f"TC_{i+1:03d}" for i in range(len(Directories))]

@pytest.mark.parametrize("directory, expected_output, testcase_num", list(zip(Directories, ExpectedOutputs, TestCaseNums)))
def test_eval(directory, expected_output, testcase_num):
	print(baseDir + directory, expected_output, testcase_num)
	
	serialResult = DiffDrives.main(baseDir + directory + "/" + targetA, baseDir + directory + "/" + targetB)
	parralelResult = ParralelDiffDrives.main(baseDir + directory + "/" + targetA, baseDir + directory + "/" + targetB)
	assert ( serialResult == expected_output)
	assert ( parralelResult == serialResult)
	