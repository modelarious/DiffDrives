import yaml
from os import sep

class YamlParser(object):
    def fetchYaml(self):
        with open("configTesting.yml", 'r') as config:
            return yaml.safe_load(config)

# object that handles interacting with the file system
class TestDataBuilder(object):
    def createFiles(self, context, filesToCreate):
        for f in filesToCreate:
            print(f"FILE: {context + sep + f}")
    
    def createDir(self, context):
        print(f"DIR: {context}")

# object that handles interpreting config and using the TestDataBuilder to 
# create the directory/file structures found in configTesting.yml for use in
# running directory testing.  The directories cannot be 
class TestDataInterpreter(object):
    def __init__(self, parsedYaml, testDataBuilder):
        self.testingConfig = parsedYaml
        self.builder = testDataBuilder
        
        self.setupKey = 'setup'
        self.filesKey = 'files'
        self.dirsKey = 'dirs'

        self.baseDir = 'Testing'
        self.DiffTargetAKey = 'DiffTargetA'
        self.DiffTargetBKey = 'DiffTargetB'
        
    def setupTestingData(self):
        for testCaseName in self.testingConfig:
            testCaseSetup = self.testingConfig[testCaseName][self.setupKey]
            self._setupTestingData(testCaseName, testCaseSetup)
    
    def _setupTestingData(self, testCaseName, testCaseSetup):
        for setupDir in [self.DiffTargetAKey, self.DiffTargetBKey]:
            context = self.baseDir + sep + testCaseName + sep + setupDir
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
        

yamlParser = YamlParser()
parsedYaml = yamlParser.fetchYaml()
testDataBuilder = TestDataBuilder()
x = TestDataInterpreter(parsedYaml, testDataBuilder)
x.setupTestingData()