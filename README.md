# DiffDrives
A tool I use to quickly compare the directory structure of two different directories, and optionally copy any files/directories that exist in directory1 to directory2.

# Usage
Compare and optionally copy files from /path/to/directory/1 to /path/to/directory/2:
`python3 DiffDrives.py /path/to/directory/1 /path/to/directory/2`

The order of arguments will need to be reversed if you want to compare in the other direction:
`python3 DiffDrives.py /path/to/directory/2 /path/to/directory/1`

# Testing
Generate test data: 

```
rm -rf Testing
python3 TestConfigParser/TestConfigParser.py
```

Run testing:

```
bash test.sh
```