import sqlite3
import datetime

class Pedido(object):
	"""
	Clase usada durante la estancia del cliente para que se vayan agregando platillos a su orden
	"""
	def __init__(self):
		self.orden = list()

	def obtenerString(self, index):
		if type(index) is int:
			s = self.orden[index]
		elif type(index) is list:
			s = index
		else:
			return ""
		return str(s[0]) + " " + str(s[1]) + "\n"

	def obtenerTotal(self):
		total = 0
		for i in orden:
			total += i[0].precio * i[1]
		return total

	def agregar(self, platillo, cantidad=1):
		index = self.contiene(platillo)
		if index != -1:
			self.orden[index][1] += 1
		else:
			s = [platillo, cantidad]
			self.orden.append(s)
		return index

	def contiene(self, platillo):
		for p in enumerate(self.orden):
			if p[1][0] == platillo:
				return p[0]
		return -1

	def get(self, index, platillo=True):
		if platillo:
			return self.orden[index][1]
		return self.orden[index]

	def __float__(self):
		return ObtenerTotal()

	def __str__(self):
		out = ""
		for s in self.orden:
			out += str(s[0]) + " " + str(s[1]) + "\n"
		return out

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
			platillo = Platillo(*sql)
		except TypeError:
			platillo = Platillo("¡ERROR! No se encontró información", "", "", "¡ERROR! No se encontró información")
		return platillo

	def confirmar(self):
		self.conexion.commit()

	def buscarTodos(self):
		"""
		Crea una lista con todos los platillos guardados en la base de datos.
		"""
		query = self.c.execute("SELECT * FROM platillosTeru")
		output = list()
		for result in query:
			try:
				output.append(Platillo(*result))
			except:
				pass
		return output
	def __len__(self):
		return self.c.lastrowid

	def getCategories(self):
		sql = self.c.execute("SELECT DISTINCT categoria FROM platillosTeru ORDER BY categoria")
		categories = list()
		for category in sql:
			categories.append(category[0])
		return categories

	def buscarCategoria(self, categoria):
		sql = self.c.execute("SELECT * FROM platillosTeru WHERE categoria LIKE '{}'".format(categoria)) 
		#TODO: Like es más lento, buscar porque no funciona =
		platillos = list()
		for s in sql:
			try:
				platillos.append( Platillo(*s))
			except TypeError:
				pass
		return platillos

