from os import path
from TestConfigParser.Constants import baseDir
class TestCaseConfigParser(object):
	def __init__(self, parsedYaml):
		self.parsedYaml = parsedYaml
		self.testCaseStorage = []
		self.tcNum = 0
		self._collectTestCases()
	
	def getTestCases(self):
		return self.testCaseStorage
	
	def _collectTestCases(self):
		for testCaseName in self.parsedYaml.keys():
			self._trackTestCase(testCaseName, self.parsedYaml[testCaseName]['expectedOutput'])

	def _trackTestCase(self, testCaseName, expectedOutput):
		self.tcNum += 1
		expectedOutputAdjusted = self._addExtendedPathInfo(testCaseName, expectedOutput)
		self.testCaseStorage.append(
			(
				testCaseName,
				expectedOutputAdjusted,
				self.tcNum
			)
		)

	def _addExtendedPathInfo(self, testCaseName, expectedOutput):
		# add the base test dir and the testCaseName dir to the front of every file and directory in expected results
		expectedOutputAdjusted = dict()
		for k, v in expectedOutput.items():
			newV = []
			for entry in v:
				newV.append(path.join(baseDir, testCaseName, entry))
			expectedOutputAdjusted[k] = sorted(newV)
		return expectedOutputAdjusted