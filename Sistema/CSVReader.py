import codecs
class CSVTable:
	def __init__(self, filename, columnsName, returnType=None):
		self.filename = filename
		self.returnType = returnType
		self.rowLenght = len(columnsName)
		with open(self.filename, "r", encoding='utf-8') as csvFile:
			line = csvFile.readline()
			self.columnsOrder = line.replace("\n","").split(",")
			if csvFile.tell() == 0:
				raise EmptyFileError
			if len(self.columnsOrder) != self.rowLenght:
				raise RowMismatchError

	def WriteRow(self, dictRow):
		if dictRow is None:
			row = str("{}," * self.rowLenght).format(*[dictRow[data] for data in self.columnsOrder])
		elif type(dictRow) is list or type(dictRow) is tuple:
			if len(dictRow) != rowLenght:
				raise RowMismatchError
			row = str("{}," * self.rowLenght).format(*dictRow)
		else:
			return 
		with open(self.filename, "a", encoding='utf8') as csvFile:
			csvFile.write("{}\n".format(row))

	def __iter__(self):
		with open(self.filename, "r", encoding='utf8') as csvFile:
			csvFile.readline()
			if self.returnType is None:
				for line in csvFile:
					yield line.replace("\n","")
			elif type(self.returnType) is tuple:
				for line in csvFile:
					yield tuple(line.replace("\n","").rstrip(",").split(","))
			elif type(self.returnType) is list:
				for line in csvFile:
					yield line.replace("\n","").rstrip(",").split(",")
			else:
				for line in enumerate(csvFile, 1):
					d = dict()
					values = line[1].replace("\n","").rstrip(",").split(",")
					for column in enumerate(self.columnsOrder):
						d[column[1]] = values[column[0]]
					yield self.returnType(d, line[0])

class EmptyFileError(Exception):
	pass

class RowMismatchError(Exception):
	pass