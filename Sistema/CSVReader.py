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
				print("Pasó! " + str(csvFile.tell()))
				raise EmptyFileError

	def WriteRow(self, dictRow):
		row = str("{}," * self.rowLenght).format(*[dictRow[data] for data in self.columnsOrder])
		with open(self.filename, "a", encoding='utf8') as csvFile:
			csvFile.write("{}\n".format(row))

	def __iter__(self):
		with open(self.filename, "r", encoding='utf8') as csvFile:
			csvFile.readline()
			if self.returnType is None:
				for line in csvFile:
					yield line.replace("\n","")
			else:
				for line in csvFile:
					d = dict()
					values = line.replace("\n","").rstrip(",").split(",")
					for column in enumerate(self.columnsOrder):
						d[column[1]] = values[column[0]]
					yield self.returnType(d)

class EmptyFileError(Exception):
	pass