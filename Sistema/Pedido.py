import sqlite3
import datetime

class Pedido(object):
	"""
	Clase usada durante la estancia del cliente para que se vayan agregando platillos a su orden
	"""
	def __init__(self):
		self.orden = list()

	def obtenerTotal(self):
		total = 0
		for i in orden:
			total += i.precio
		return total

	def agregar(self, platillo):
		self.orden.append(platillo)

	def __float__(self):
		return ObtenerTotal()

class Platillo(object):
	"""
	Clase ocupada para almacenar información de los platillos
	"""
	def __init__(self, nombre, precio, categoria, idPlatillo=-1):
		self.nombre = nombre
		self.precio = precio
		self.categoria = categoria
		self.idPlatillo = idPlatillo

	def __str__(self):
		return "{:3d} {:30s} ${:5.2f} {:10s}".format(self.idPlatillo, self.nombre, self.precio, self.categoria)

class PlatilloDB:

	def __init__(self, conexion):
		self.conexion = conexion
		self.c = self.conexion.cursor()

		self.c.execute("""CREATE TABLE IF NOT EXISTS platillosTeru 
			( nombre VARCHAR, 
			precio REAL, 
			categoria VARCHAR,
			id INTEGER PRIMARY KEY)""")

	def insertar(self, platillo):
		sql = \
		"""INSERT INTO platillosTeru(nombre, precio, categoria)
		VALUES('{}', {}, '{}')""".format(platillo.nombre, platillo.precio, platillo.categoria)
		self.c.execute(sql)

	def actualizar(self, identificador, nombre="", precio="", categoria=""):
		if nombre == "" and precio == "" and categoria == "":
			return
		sql = "UPDATE platillosTeru SET "
		if nombre:
			sql += "nombre = '{}', ".format(nombre)
		if precio:
			sql += "precio = '{}', ".format(precio)
		if categoria:
			sql += "categoria = '{}', ".format(categoria)

		sql = sql[0:-2] + " WHERE id={}".format(identificador)
		self.c.execute(sql)

	def borrar(self, identificador):
		self.c.execute("DELETE FROM platillosTeru WHERE id={}".format(identificador))

	def buscarID(self,identificador):
		"""
		Busca en la tabla por ID y retorna el primer valor encontrado
		"""
		sql = self.c.execute("SELECT * FROM platillosTeru WHERE id='{}'".format(identificador)).fetchone()
		try:
			cliente = Platillo(*sql)
		except TypeError:
			cliente = Platillo("¡ERROR! No se encontró información", "", "", "¡ERROR! No se encontró información")
		return cliente

	def confirmar(self):
		self.conexion.commit()

	def buscarTodos(self):
		"""
		Crea una lista con todos los platillos guardados en la base de datos.
		"""
		query = self.c.execute("SELECT * FROM platillosTeru").fetchall()
		output = list()
		for result in query:
			try:
				output.append(Platillo(*result))
			except:
				pass
		return output
	def __len__(self):
		return self.c.lastrowid
