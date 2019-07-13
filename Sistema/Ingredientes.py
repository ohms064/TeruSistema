from Sistema.ObjectDB import *
from Sistema.Platillo import *

class Ingrediente:
	def __init__(self, idIngrediente=-1, nombre="" ,precio=0, cantidad=0, unidadCantidad="", lugar = ""):
		self.idIngrediente = idIngrediente
		self.nombre = nombre
		self.precio = precio
		self.cantidad = cantidad
		self.unidadCantidad = unidadCantidad
		self.lugar = lugar

	def __str__(self):
		return "{:3d}, {}".format(self.idIngrediente, self.nombre)

	def toTuple(self):
		return (self.nombre, self.precio, self.cantidad, self.unidadCantidad)

class IngredientePlatillo:
	def __init__(self, idUnion=-1, idIngrediente=-1, idPlatillo=-1, porcion=0, unidadPorcion="", extra=False):
		self.idUnion = idUnion
		self.idIngrediente = idIngrediente
		self.idPlatillo = idPlatillo
		self.porcion = porcion
		self.unidadPorcion = unidadPorcion
		self.extra = extra
		self.ingrediente = None
		self.platillo = None

	def setIngrediente(self, ingrediente):
		self.ingrediente = ingrediente

	def setPlatillo(self, platillo):
		self.platillo = platillo

	def __str__(self):
		if self.ingrediente is None:
			return ""
		return str(self.ingrediente)

class IngredienteDB(ObjectDB):
	def __init__(self, conexion):
		super().__init__(conexion)
		self.c.execute("""CREATE TABLE IF NOT EXISTS ingredienteTeru(
			id INTEGER PRIMARY KEY,
			nombre VARCHAR,
			precio REAL,
			cantidad REAL,
			idUnidad INTEGER,
			lugar VARCHAR,
			UNIQUE(nombre),
			FOREIGN KEY(idUnidad) REFERENCES unidadTeru(id)
			)""")
		self.c.execute("""CREATE TABLE IF NOT EXISTS ingrediente_platillo_Teru(
			id INTEGER PRIMARY KEY,
			idPlatillo INTEGER,
			idIngrediente INTEGER,
			porcion REAL,
			idUnidad INTEGER,
			extra INTEGER,
			FOREIGN KEY(idPlatillo) REFERENCES platilloTeru(id),
			FOREIGN KEY(idUnidad) REFERENCES unidadTeru(id),
			FOREIGN KEY(idIngrediente) REFERENCES ingredienteTeru(id),
			UNIQUE(idPlatillo, idIngrediente)
			)""")

	def insertarIngrediente(self, ingrediente):
		sql = "SELECT id FROM unidadTeru WHERE nombre = ?"
		idUnidad = self.c.execute(sql, (ingrediente.unidadCantidad, )).fetchone()[0]
		sql = "INSERT OR REPLACE INTO ingredienteTeru(nombre, precio, cantidad, idUnidad) VALUES(?, ?, ?, ?)"
		self.c.execute(sql, (ingrediente.nombre, ingrediente.precio, ingrediente.cantidad, idUnidad))

	def insertarVariosIngredientes(self, ingredientes):
		sql = "SELECT id FROM unidadTeru WHERE nombre = ?"
		tuplaIngredientes = list()
		for i in range(len(ingredientes)):
			unidad = self.c.execute(sql, (ingredientes[i].unidadCantidad, )).fetchone()[0]
			ingredientes[i].unidadCantidad = unidad
			tuplaIngredientes.append(ingredientes[i].toTuple())

		sql = "INSERT OR REPLACE INTO ingredienteTeru(nombre, precio, cantidad, idUnidad) VALUES(?, ?, ?, ?)"
		self.c.executemany(sql, tuple(tuplaIngredientes))

	def insertarIngredientePlatillo(self, ingredientePlatillo):
		sql = "SELECT id FROM unidadTeru WHERE nombre = ?"
		idUnidad = self.c.execute(sql, (ingredientePlatillo.unidadPorcion,))
		sql = "INSERT OR IGNORE INTO ingrediente_platillo_Teru(idPlatillo, idIngrediente, porcion, idUnidad, extra) VALUES(?, ?, ?, ?, ?)"
		self.c.execute(sql, (ingredientePlatillo.idPlatillo, ingredientePlatillo.idIngrediente, ingredientePlatillo.porcion, idUnidad, ingredientePlatillo.extra))

	def actualizarIngrediente(self, identificador, nombre="", precio="", cantidad="", idUnidad="", lugar=""):
		if nombre == "" and precio == "" and categoria == "" and plugin == "":
			return False
		sql = "UPDATE ingredienteTeru SET "
		if nombre:
			sql += "nombre = '{}', ".format(nombre)
		if precio:
			sql += "precio = {}, ".format(precio)
		if cantidad:
			sql += "cantidad = {}, ".format(cantidad)
		if idUnidad:
			sql += "idUnidad = '{}', ".format(idUnidad)
		if lugar:
			sql += "lugar = '{}', ".format(lugar)

		sql = sql[0:-2] + " WHERE id={}".format(identificador)
		print(sql)
		self.c.execute(sql)
		return True

	def borrarTodoIngrediente(self):
		self.c.execute("DELETE FROM ingredienteTeru")

	def actualizarIngredientePlatillo(self, porcion="", idUnidad="", extra=None):
		if porcion == "" and idUnidad == "" and extra == "":
			return False
		sql = "UPDATE ingrediente_platillo_Teru SET "
		if porcion:
			porcion += "nombre = {}, ".format(porcion)
		if idUnidad:
			idUnidad += "nombre = {}, ".format(idUnidad)
		if extra is not None: #Entonces es booleano
			extra += "nombre = {}, ".format(int(extra))

		sql = sql[0:-2] + " WHERE id={}".format(identificador)
		self.c.execute(sql)
		return True

	def buscarID(self,identificador):
		"""
		Busca en la tabla por ID y retorna el primer valor encontrado
		"""
		query = """SELECT * FROM ingredienteTeru 
			JOIN unidadTeru ON unidadTeru.id = ingredienteTeru.idUnidad 
			WHERE id={}""".format(identificador)
		sql = self.c.execute(query).fetchone()
		try:
			ingrediente = Ingrediente(*sql)
		except TypeError:
			ingrediente = Ingrediente("¡ERROR! No se encontró información", "", "", "¡ERROR! No se encontró información","")
		return ingrediente

	def buscarTodos(self):
		result = list()
		sqlRes = self.c.execute("SELECT * FROM ingredienteTeru")
		for ing in sqlRes:
			result.append(Ingrediente(*ing))
		return result

	def buscarIngredientesFromPlatillo(self, identificador):
		result = []
		query = """SELECT * FROM platilloTeru 
		JOIN ingrediente_platillo_Teru ON platilloTeru.id = ingrediente_platillo_Teru.idPlatillo
		JOIN ingredienteTeru ON ingredienteTeru.id = ingrediente_platillo_Teru.idIngrediente
		WHERE platilloTeru.id = ?"""
		sql = self.c.execute(query, (identificador,))

		for s in sql:
			result.append(self.createIngredientePlatillo(s))
		return result

	def borrarIngrediente(self, identificador):
		self.c.execute("DELETE FROM ingredienteTeru WHERE id = ?",(identificador,))

	def borrarIngredientePlatillo(self, idPlatillo, idIngrediente=None):
		if idIngrediente is None:
			self.c.execute("DELETE FROM ingrediente_platillo_Teru WHERE id=?",(idPlatillo,))
		else:
			self.c.execute("DELETE FROM ingrediente_platillo_Teru WHERE idPlatillo = ? AND idIngrediente = ?",(idPlatillo, idIngrediente))

	def buscarIngredientePlatillo(self, idPlatillo, idIngrediente=None):
		if idIngrediente is None:
			query = """SELECT * FROM platilloTeru 
				JOIN ingrediente_platillo_Teru ON platilloTeru.id = ingrediente_platillo_Teru.idPlatillo
				JOIN ingredienteTeru ON ingredienteTeru.id = ingrediente_platillo_Teru.idIngrediente
				WHERE platilloTeru.id = ?"""
			result = self.c.execute(query ,(idPlatillo,))
		else:
			query = """SELECT * FROM platilloTeru 
				JOIN ingrediente_platillo_Teru ON platilloTeru.id = ingrediente_platillo_Teru.idPlatillo
				JOIN ingredienteTeru ON ingredienteTeru.id = ingrediente_platillo_Teru.idIngrediente
				WHERE idPlatillo = ? AND idIngrediente = ?"""
			result = self.c.execute(query ,(idPlatillo, idIngrediente))
		return createIngredientePlatillo(result)

	def createIngredientePlatillo(self, sql):
		ing = IngredientePlatillo(*sql[5:11])
		ing.setIngrediente(Ingrediente(*sql[11:]))
		ing.setPlatillo(Platillo(*sql[:5]))
		return ing

def ingredienteCSVSerializer(csv, pos):
	return Ingrediente(pos, csv["Nombre"], csv["Precio"], csv["Cantidad"], csv["Unidad"])