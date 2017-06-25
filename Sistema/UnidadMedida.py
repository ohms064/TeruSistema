from Sistema.ObjectDB import *
class Unidad:
	def __init__(self ,idUnidad, nombre, valor):
		self.idUnidad = idUnidad
		self.nombre = nombre
		self.valor = valor

class UnidadDB(ObjectDB):
	def __init__(self, conexion):
		super().__init__(conexion)
		self.c.execute("""
			CREATE TABLE IF NOT EXISTS unidadTeru(
			id INTEGER PRIMARY KEY,
			nombre TEXT,
			valor REAL
			)
			""")

	def insertar(self, unidad):
		sql = """ INSERT OR REPLACE INTO unidadTeru(nombre, valor) VALUES (?, ?) """
		self.c.execute(sql, (unidad.nombre, unidad.valor))

	def obtenerTodos(self):
		unidades = list()
		sql = self.c.execute(""" SELECT * FROM unidadTeru """)
		for unidad in sql:
			unidades.append(Unidad(*unidad))
		return unidades

	def inicializar(self):
		unidades = ((1, "mg", 1000), (2, "g", 1), (3, "kg", .01), (4, "l", 1), (5, "ml", 1000))
		sql = """ INSERT OR REPLACE INTO unidadTeru(id, nombre, valor) VALUES (?, ?, ?) """
		self.c.executemany(sql, unidades)
		self.unidades = self.obtenerTodos()
		self.nombres = [unidad.nombre for unidad in self.unidades]
