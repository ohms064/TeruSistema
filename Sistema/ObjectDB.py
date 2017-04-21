class ObjectDB:
	def __init__(self, conexion):
		self.conexion = conexion
		self.c = self.conexion.cursor()

	def confirmar(self):
		self.conexion.commit()

	def rewind(self):
		self.c.rollback()

	def cerrar(self):
		self.conexion.close()

	def __len__(self):
		return self.c.lastrowid

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.cerrar()