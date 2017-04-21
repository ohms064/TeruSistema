from Sistema.ObjectDB import *
import sqlite3

class Platillo(object):
	"""
	Clase ocupada para almacenar información de los platillos, el orden de los argumentos es importante.
	"""
	def __init__(self, nombre, precio, categoria, idPlatillo=-1, pluginName="general.json", extra=0):
		self.nombre = nombre
		self.precio = precio
		self.categoria = categoria.lower()
		self.idPlatillo = idPlatillo
		self.pluginName = pluginName
		self.extra = extra

	def __str__(self):
		return "{:3d} {:<50} ${:5.2f}    {:10s}".format(self.idPlatillo, self.nombre, self.precio, self.categoria)

class PlatilloDB(ObjectDB):

	def __init__(self, conexion):
		super().__init__(conexion)

		self.c.execute("""CREATE TABLE IF NOT EXISTS platilloTeru 
			( nombre VARCHAR, 
			precio REAL, 
			categoria VARCHAR,
			id INTEGER PRIMARY KEY,
			plugin VARCHAR)""")

	def insertar(self, platillo):
		sql = \
		"""INSERT INTO platilloTeru(nombre, precio, categoria, plugin)
		VALUES('{}', {}, '{}', '{}')""".format(platillo.nombre, platillo.precio, platillo.categoria, platillo.pluginName)
		self.c.execute(sql)

	def actualizar(self, identificador, nombre="", precio="", categoria="", plugin=""):
		if nombre == "" and precio == "" and categoria == "" and plugin == "":
			return False
		sql = "UPDATE platilloTeru SET "
		if nombre:
			sql += "nombre = '{}', ".format(nombre)
		if precio:
			sql += "precio = '{}', ".format(precio)
		if categoria:
			sql += "categoria = '{}', ".format(categoria)
		if plugin:
			sql += "plugin = '{}', ".format(plugin)

		sql = sql[0:-2] + " WHERE id={}".format(identificador)
		print(sql)
		self.c.execute(sql)
		return True

	def borrar(self, identificador):
		self.c.execute("DELETE FROM platilloTeru WHERE id={}".format(identificador))

	def borrarTodo(self):
		self.c.execute("DELETE FROM platilloTeru")

	def buscarID(self,identificador):
		"""
		Busca en la tabla por ID y retorna el primer valor encontrado
		"""
		sql = self.c.execute("SELECT * FROM platilloTeru WHERE id='{}'".format(identificador)).fetchone()
		try:
			platillo = Platillo(*sql)
		except TypeError:
			platillo = Platillo("¡ERROR! No se encontró información", "", "", "¡ERROR! No se encontró información")
		return platillo

	def buscarTodos(self):
		"""
		Crea una lista con todos los platillos guardados en la base de datos.
		"""
		query = self.c.execute("SELECT * FROM platilloTeru")
		output = list()
		for result in query:
			try:
				output.append(Platillo(*result))
			except:
				pass
		return output

	def getCategories(self):
		sql = self.c.execute("SELECT DISTINCT categoria FROM platilloTeru ORDER BY categoria")
		categories = list()
		for category in sql:
			categories.append(category[0])
		return categories

	def buscarCategoria(self, categoria):
		sql = self.c.execute("SELECT * FROM platilloTeru WHERE categoria LIKE '{}'".format(categoria)) 
		#TODO: Like es más lento, buscar porque no funciona =
		platillos = list()
		for s in sql:
			try:
				platillos.append( Platillo(*s))
			except TypeError:
				pass
		return platillos

def platilloCsvSerializer(values):
	return Platillo(values["Platillo"], values["Precio"], values["Categoría"], pluginName=values["Plugin"])

class CustomPlatilloDB(ObjectDB):
	def __init__(self, conexion):
		super().__init__(conexion)
		self.c.execute("""CREATE TABLE IF NOT EXISTS platilloTeru 
			( 
			id INTEGER PRIMARY KEY
			idBasePlatillo INTEGER
			nombre VARCHAR
			extraPrecio
			)""")