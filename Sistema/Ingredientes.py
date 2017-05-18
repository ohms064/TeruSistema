from Sistema.ObjectDB import *
from Sistema.Platillo import *

class Ingrediente:
	def __init__(self, idIngrediente=-1, nombre="" ,precio=0, cantidad=0, unidadCantidad="", ):
		self.idIngrediente = idIngrediente
		self.nombre = nombre
		self.precio = precio
		self.cantidad = cantidad
		self.unidadCantidad = unidadCantidad

	def __str__(self):
		return "{:3d}, {}".format(self.idIngrediente, self.nombre)

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
			unidad VARCHAR,
			UNIQUE(nombre)
			)""")
		self.c.execute("""CREATE TABLE IF NOT EXISTS ingrediente_platillo_Teru(
			id INTEGER PRIMARY KEY,
			idPlatillo INTEGER,
			idIngrediente INTEGER,
			porcion REAL,
			unidad VARCHAR,
			extra INTEGER,
			FOREIGN KEY(idPlatillo) REFERENCES platilloTeru(id),
			FOREIGN KEY(idIngrediente) REFERENCES ingredienteTeru(id),
			UNIQUE(idPlatillo, idIngrediente)
			)""")

	def insertarIngrediente(self, ingrediente):
		sql = "INSERT OR REPLACE INTO ingredienteTeru(nombre, precio, cantidad, unidad) VALUES(?, ?, ?, ?)"
		self.c.execute(sql, (ingrediente.nombre, ingrediente.precio, ingrediente.cantidad, ingrediente.unidadCantidad))

	def insertarVariosIngredientes(self, ingredientes):
		sql = "INSERT OR REPLACE INTO ingredienteTeru(nombre, precio, cantidad, unidad) VALUES(?, ?, ?, ?)"
		self.c.executemany(sql, ingredientes)

	def insertarIngredientePlatillo(self, ingredientePlatillo):
		sql = "INSERT OR IGNORE INTO ingrediente_platillo_Teru(idPlatillo, idIngrediente, porcion, unidad, extra) VALUES(?, ?, ?, ?, ?)"
		self.c.execute(sql, (ingredientePlatillo.idPlatillo, ingredientePlatillo.idIngrediente, ingredientePlatillo.porcion, ingredientePlatillo.unidadPorcion, ingredientePlatillo.extra))

	def actualizarIngrediente(self, identificador, nombre="", precio="", cantidad="", unidad=""):
		if nombre == "" and precio == "" and categoria == "" and plugin == "":
			return False
		sql = "UPDATE ingredienteTeru SET "
		if nombre:
			sql += "nombre = '{}', ".format(nombre)
		if precio:
			sql += "precio = {}, ".format(precio)
		if cantidad:
			sql += "cantidad = {}, ".format(cantidad)
		if unidad:
			sql += "unidad = '{}', ".format(unidad)

		sql = sql[0:-2] + " WHERE id={}".format(identificador)
		print(sql)
		self.c.execute(sql)
		return True

	def borrarTodoIngrediente(self):
		self.c.execute("DELETE FROM ingredienteTeru")

	def actualizarIngredientePlatillo(self, porcion="", unidad="", extra=None):
		if porcion == "" and unidad == "" and extra == "":
			return False
		sql = "UPDATE ingrediente_platillo_Teru SET "
		if porcion:
			porcion += "nombre = {}, ".format(porcion)
		if unidad:
			unidad += "nombre = {}, ".format(unidad)
		if extra is not None: #Entonces es booleano
			extra += "nombre = {}, ".format(int(extra))

		sql = sql[0:-2] + " WHERE id={}".format(identificador)
		self.c.execute(sql)
		return True

	def buscarID(self,identificador):
		"""
		Busca en la tabla por ID y retorna el primer valor encontrado
		"""
		sql = self.c.execute("SELECT * FROM ingredienteTeru WHERE id={}".format(identificador)).fetchone()
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
	import pdb; pdb.set_trace()  # breakpoint 8d2996a7 //
	return Ingrediente(pos, csv["Nombre"], csv["Precio"], csv["Cantidad"], csv["Unidad"])