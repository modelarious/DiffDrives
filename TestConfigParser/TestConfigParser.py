from TestDataBuilder import TestDataBuilder
from YamlReader import YamlReader
from TestDataInterpreter import TestDataInterpreter

class TestConfigParser(object):
    def __init__(self):
        testDataBuilder = TestDataBuilder()
        parsedYaml = YamlReader().fetchYaml("configTesting.yml")

        interpreter = TestDataInterpreter(parsedYaml, testDataBuilder)
        interpreter.setupTestingData()

TestConfigParser()