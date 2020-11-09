from os import sep

from Constants import BaseDir, TargetA, TargetB

# object that handles interpreting config and using the TestDataBuilder to 
# create the directory/file structures found in configTesting.yml for use in
# running directory testing.
class ConfigInterpreter(object):
    def __init__(self, parsedYaml, testDataBuilder):
        self.testingConfig = parsedYaml
        self.builder = testDataBuilder
        
        self.setupKey = 'setup'
        self.filesKey = 'files'
        self.dirsKey = 'dirs'
        
    def setupTestingData(self):
        for testCaseName in self.testingConfig:
            testCaseSetup = self.testingConfig[testCaseName][self.setupKey]
            self._setupTestingData(testCaseName, testCaseSetup)
    
    def _setupTestingData(self, testCaseName, testCaseSetup):
        for setupDir in [TargetA, TargetB]:
            context = BaseDir + sep + testCaseName + sep + setupDir
            currentSetup = testCaseSetup[setupDir]
            self._handleDirectory(context, currentSetup)

    def _handleDirectory(self, context, directory):
        print(f"\n\ndirectory = {directory}, context={context}")

        # create current directory
        self.builder.createDir(context)
        
        # exit early if the directory is None (directory has no contents)
        if directory == None:
            return

        # if there are files in the directory, create them
        if self.filesKey in directory:
            self.builder.createFiles(context, directory[self.filesKey])
        
        # if there are directories in the directory, recurse and create them too
        if self.dirsKey in directory:
            for subDirName, subDirContents in directory[self.dirsKey].items():
                self._handleDirectory(context + sep + subDirName, subDirContents)