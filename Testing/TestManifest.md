#Tests

##Directory Tests
###SameDirectoryStructureFlat (TC_001):

- Both diff targets have the same directory structure and contain no files
- Directory structure is flat (depth of 1)

expected outcome:

- DiffDrives finds no differences between the two structures and returns 0

###SameDirectoryStructureNested (TC_002):

- Both diff targets have the same directory structure and contain no files
- Directory structure is nested (depth of 2)

expected outcome:

- DiffDrives finds no differences between the two structures and returns 0

###DifferentDirectoryStructureFlat (TC_003):

- Diff Target B is missing a directory from Diff Target A, contains no files
- Directory structure is flat (depth of 1)

expected outcome:

- DiffDrives reports the missing directory and returns -1

###DifferentDirectoryStructureNested (TC_004):

- Diff Target B is missing a nested directory from Diff Target A, contains no files
- Directory structure is nested (depth of 2)

expected outcome:

- DiffDrives reports the missing directory and returns -1

##File Tests
###SameFilesFlat (TC_005):

- Both diff targets have the same files

expected outcome:

- DiffDrives finds no differences between the two targets and returns 0

###SameFilesNested (TC_006):

- Both diff targets have the same files and directory structure
- Directory structure is nested (depth of 2)
- Files appear 2 directories deep

expected outcome:

- DiffDrives finds no differences between the two targets and returns 0

###DifferentFilesFlat (TC_007):

- A file is missing from Diff Target B

expected outcome:

- DiffDrives reports the missing file and returns -1

###DifferentFilesNested (TC_008):

- There is a nested file missing from Diff Target B
- Directory structure is nested (depth of 2)
- Files appear 2 directories deep

expected outcome:

- DiffDrives reports the missing file and returns -1

##Combined Tests
###DifferentDirectoryStructureDifferentFilesFlat (TC_009):

- There is a file and directory missing from Diff Target B
- Directory structure is flat (depth of 1)

expected outcome:

- DiffDrives reports the missing file and directory and returns -1

###DifferentDirectoryStructureDifferentFilesNested (TC_010):

- There is a nested file and nested directory missing from Diff Target B
- Directory structure is nested (depth of 2)

expected outcome:

- DiffDrives reports the missing file and directory and returns -1

###HardTest (TC_666):

- There is a file and directory at root that is missing, as well as several nested files and nested directories at various depths missing from Diff Target B
- Directory structure is deeply nested (depth of 4)

expected outcome:

- DiffDrives reports the missing files and directories and returns -1