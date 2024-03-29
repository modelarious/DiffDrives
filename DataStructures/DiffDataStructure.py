from Logging import printSTATUS
# separate data storage logic from the class logic
class DiffDataStructure(object):
	
	def __init__(self):
		self.filesKey = "files"
		self.dirsKey = "dirs"
		
		# track files and dirs that differ between the two sources
		self.diff = {self.filesKey:[], self.dirsKey:[]}
	
	def trackFiles(self, files):
		printSTATUS("extending the tracked files by", files)
		self.diff[self.filesKey].extend(files)
	
	def trackDirs(self, dirs):
		printSTATUS("extending the tracked dirs by", dirs)
		self.diff[self.dirsKey].extend(dirs)
	
	def getDiff(self):
		sortedDiff = {
			self.filesKey: sorted(self.diff[self.filesKey]),
			self.dirsKey: sorted(self.diff[self.dirsKey])
		}
		self.diff = sortedDiff
		return self.diff
	
	def getFiles(self):
		return self.diff[self.filesKey]
	
	def getDirectories(self):
		return self.diff[self.dirsKey]