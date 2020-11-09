from TestDataBuilder import TestDataBuilder
from YamlReader import YamlReader
from ConfigInterpreter import ConfigInterpreter

class TestConfigParser(object):
    def __init__(self):
        testDataBuilder = TestDataBuilder()
        parsedYaml = YamlReader().fetchYaml("configTesting.yml")

        interpreter = ConfigInterpreter(parsedYaml, testDataBuilder)
        interpreter.setupTestingData()

TestConfigParser()