from abc import ABC, abstractmethod
class FetchDirectoryInfoAbstract(ABC):
	@abstractmethod
	def getDirectoryInfo(self, path):
		return None