import sqlite3
import datetime
import json

class Pedido(object):
	"""
	Clase usada durante la estancia del cliente para que se vayan agregando platillos a su orden
	"""
	def __init__(self):
		self.orden = list()

	def obtenerString(self, index):
		"""
		Obtiene la cadena de un elemento de orden ya sea pasando un elemento o un índice que buscar en la variable
		"""
		if type(index) is int:
			s = self.orden[index]
		elif type(index) is list:
			s = index
		else:
			return ""
		return str(s[0]) + " " + str(s[1]) + "\n"

	def obtenerTotal(self):
		total = 0

		for i in self.orden:
			total += i[0].precio * i[1]
		return total

	def agregar(self, platillo, cantidad=1, byString=False, byId=False):
		"""
		Agrega un platillo a la orden, si este platillo ya se encuentra en la orden se aumenta la cantidad
		"""
		if byString:
			index = self.findByString(platillo.nombre)
		elif byId:
			index = self.findById(platillo.platilloId)
		else:
			index = self.contiene(platillo)

		if index != -1:
			self.orden[index][1] += cantidad
		else:
			s = [platillo, cantidad]
			self.orden.append(s)
		return index

	def contiene(self, platillo):
		for p in enumerate(self.orden):
			if p[1][0] == platillo:
				return p[0]
		return -1

	def findByString(self, nombrePlatillo):
		for p in enumerate(self.orden):
			if p[1][0].nombre == nombrePlatillo:
				return p[0]
		return -1		

	def findById(self, idPlatillo):
		for p in enumerate(self.orden):
			if p[1][0].idPlatillo == idPlatillo:
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
	Clase ocupada para almacenar información de los platillos, el orden de los argumentos es importante.
	"""
	def __init__(self, nombre, precio, categoria, idPlatillo=-1, pluginName="general.json"):
		self.nombre = nombre
		self.precio = precio
		self.categoria = categoria.lower()
		self.idPlatillo = idPlatillo
		self.pluginName = pluginName

	def __str__(self):
		return "{:3d} {:<50} ${:5.2f}    {:10s}".format(self.idPlatillo, self.nombre, self.precio, self.categoria)

class PlatilloDB:

	def __init__(self, conexion):
		self.conexion = conexion
		self.c = self.conexion.cursor()

		self.c.execute("""CREATE TABLE IF NOT EXISTS platillosTeru 
			( nombre VARCHAR, 
			precio REAL, 
			categoria VARCHAR,
			id INTEGER PRIMARY KEY,
			plugin VARCHAR)""")

	def insertar(self, platillo):
		sql = \
		"""INSERT INTO platillosTeru(nombre, precio, categoria, plugin)
		VALUES('{}', {}, '{}', '{}')""".format(platillo.nombre, platillo.precio, platillo.categoria, platillo.pluginName)
		self.c.execute(sql)

	def actualizar(self, identificador, nombre="", precio="", categoria="", plugin=""):
		if nombre == "" and precio == "" and categoria == "" and plugin == "":
			return False
		sql = "UPDATE platillosTeru SET "
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
		self.c.execute("DELETE FROM platillosTeru WHERE id={}".format(identificador))

	def borrarTodo(self):
		self.c.execute("DELETE FROM platillosTeru")

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

	def deshacer(self):
		self.conexion.rollback()

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

def platilloCsvSerializer(values):
	return Platillo(values["Platillo"], values["Precio"], values["Categoría"], pluginName=values["Plugin"])
