import sqlite3
import datetime
import json
from Sistema.ObjectDB import *

class Pedido(object):
	"""
	Clase usada durante la estancia del cliente para que se vayan agregando platillos a su orden
	"""
	def __init__(self, fecha, orden=None, idCliente=-1):
		if orden is None:
			self.orden = list()
		else:
			self.orden = orden
		self.idCliente = idCliente
		self.fecha = fecha

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

	def withCliente(self, idCliente):
		self.idCliente = idCliente

	def clear(self):
		self.orden = list()

class PedidoDB(ObjectDB):
	def __init__(self, conexion):
		super().__init__(conexion)

		self.c.execute("""CREATE TABLE IF NOT EXISTS ordenTeru 
			(
			id INTEGER PRIMARY KEY,
			idCliente INTEGER,
			fecha DATE,
			FOREIGN KEY(idCliente) REFERENCES clienteTeru(id)
			)""")

		self.c.execute("""CREATE TABLE IF NOT EXISTS orden_platillo_Teru
			(
			id INTEGER PRIMARY KEY,
			idOrden INTEGER,
			idPlatillo INTEGER,
			cantidad INTEGER,
			extras REAL,
			FOREIGN KEY(idOrden) REFERENCES ordenTeru(id),
			FOREIGN KEY(idPlatillo) REFERENCES platilloTeru(id)
			)""")

	def insertarPedido(self, pedido):
		if pedido.idCliente == -1:
			sql = " INSERT INTO ordenTeru(fecha) VALUES (?)"
			self.c.execute(sql, (pedido.fecha, ))
		else:
			sql = " INSERT INTO ordenTeru(idCliente, fecha) VALUES (?, ?)"
			self.c.execute(sql, (pedido.idCliente, pedido.fecha, ))
		print(sql)
		lastId = self.c.lastrowid
		for platillo in pedido.orden:
			sql = " INSERT INTO orden_platillo_Teru(idOrden, idPlatillo, cantidad, extras) VALUES ({}, {}, {}, {})".format(lastId, platillo[0].idPlatillo, platillo[1], platillo[0].extra)
			self.c.execute(sql)

	def buscarTodos(self):
		pass

	def buscarOrden(self, idOrden):
		query = "SELECT * FROM ordenTeru JOIN orden_platillo_Teru ON ordenTeru.id = orden_platillo_Teru.idOrden WHERE ordenTeru.id = ?"
		self.c.execute(query, (idOrden,))
		#TODO: Ordenar la información obtenida