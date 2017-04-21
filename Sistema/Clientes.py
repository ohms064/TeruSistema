import sqlite3
import datetime
from Sistema.ObjectDB import *
class ClienteTeru:
	def __init__(self, sql):
		"""
		Recibe los datos de una consulta de ClienteDB y sólo ClienteDB a menos que los datos se envíen 
		en una tupla como sigue: id, nombre, consumo, visitas, ultimaVisita, correo, nick
		"""
		try:
			self.id = sql[0]
			self.nombre = sql[1]
			self.consumo = sql[2]
			self.visitas = sql[3]
			self.ultimaVisita = sql[4]
			self.correo = sql[5]
			self.nick = sql[6]
			self.fechaIngreso = sql[7]
		except TypeError as et:
			self.id = "¡ERROR! No se encontró información"
			self.nombre = self.id
			self.consumo = self.id
			self.visitas = self.id
			self.ultimaVisita = self.id
			self.correo = self.id
			self.nick = self.id
			self.fechaIngreso = self.id

	def beautifulString(self):
		if self:
			return "ID: " + str(self.id) + "\nNombre: " + str(self.nombre) + "\nVisitas: " + str(self.visitas) + "\nCorreo: " + str(self.correo) + "\nNick: " + str(self.nick)
		return ""

	def __str__(self):
		return str(self.id) + "," + str(self.nombre) + "," + str(self.consumo) + "," + str(self.visitas) + " ," + str(self.ultimaVisita) + "," + str(self.correo) + "," + str(self.nick)

	def __bool__(self):
		return self.id != "¡ERROR! No se encontró información"

class ClienteDB(ObjectDB):
	def __init__(self, conexion):
		super().__init__(conexion)
		
		self.c.execute("""CREATE TABLE IF NOT EXISTS clienteTeru 
			( id INTEGER PRIMARY KEY, 
			nombre VARCHAR, 
			consumo REAL, 
			visitas INTEGER, 
			ultimaVisita VARCHAR, 
			correo VARCHAR, 
			nick VARCHAR, 
			fechaIngreso VARCHAR)""")
	
	def insertar(self, nombre, consumo=0, correo="", nick="", ultimaVisita="0-0-0", visitas=1, fechaIngreso="0-0-0"):
		if ultimaVisita == "0-0-0":
			fecha = datetime.datetime.now()
			ultimaVisita = str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year)
		if fechaIngreso == "0-0-0":
			fecha = datetime.datetime.now()
			fechaIngreso = str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year)

		sql = \
		"""INSERT INTO clienteTeru(nombre, consumo, visitas, ultimaVisita, correo, nick, fechaIngreso) 
		VALUES ('{}', {}, {}, '{}', '{}', '{}', '{}')""".format(nombre, consumo, visitas, ultimaVisita, correo, nick, fechaIngreso)
		self.c.execute(sql)

	def actualizar(self, identificador, nombre="", nick="", correo=""):
		"""
		Función para actualizar los datos de un cliente con un identificador.
		"""	
		if nombre == "" and nick == "" and correo == "":#Seguramente esto se puede mejorar usando **args
			return
		sql = "UPDATE clienteTeru SET "
		if nombre != "":
			sql += "nombre = '{}', ".format(nombre)
		if nick != "":
			sql += "nick = '{}', ".format(nick)
		if correo != "":
			sql += "correo = '{}', ".format(correo)
		sql = sql[0:-2] + " WHERE id={}".format(identificador)
		self.c.execute(sql)

	def borrar(self, identificador):
		self.c.execute("DELETE FROM clienteTeru WHERE id={}".format(identificador))

	def buscarID(self,ide):
		"""
		Busca en la tabla por ID y retorna el primer valor encontrado
		"""
		return ClienteTeru(self.c.execute("SELECT * FROM clienteTeru WHERE id='{}'".format(ide)).fetchone())

	def buscarNombre(self, nombre):
		"""
		Busca en la tabla por nombre y retorna el primer valor encontrado
		"""
		return ClienteTeru(self.c.execute("SELECT * FROM clienteTeru WHERE nombre='{}'".format(nombre)).fetchone())

	def buscarNick(self, nick):
		"""
		Busca en la tabla por nick y retorna el primer valor encontrado
		"""
		return ClienteTeru(self.c.execute("SELECT * FROM clienteTeru WHERE nick='{}'".format(nick)).fetchone())

	def resetVisitas(self):
		"""
		Resetea a todos los clientes su valor de visitas a 0. Esto para que se haga cada mes.
		"""
		self.c.execute(" UPDATE clienteTeru SET visitas = 0")

	def resetConsumo(self):
		"""
		Resetea a todos los clientes su valor de visitas a 0. Esto para que se haga cada mes.
		"""
		self.c.execute(" UPDATE clienteTeru SET consumo = 0")

	def incVisitas(self, identificador):
		"""
		Se incrementa el valor de las visitas por 1.
		"""
		self.c.execute(" UPDATE clienteTeru SET visitas = visitas + 1 WHERE id={}".format(identificador))

	def incConsumo(self, identificador, consumo):
		self.c.execute(" UPDATE clienteTeru SET consumo = consumo + {} WHERE id={}".format(consumo, identificador))	

	def actualizarUltimaVisita(self, identificador, fecha):
		self.c.execute(" UPDATE clienteTeru SET ultimaVisita = {} WHERE id={}".format(fecha, identificador))			

	def buscarCorreo(self, correo):
		"""
		Busca en la tabla por correo y retorna el primer valor encontrado
		"""
		return ClienteTeru(self.c.execute("SELECT * FROM clienteTeru WHERE correo='{}'".format(correo)).fetchone())

	def drop(self):
		self.c.execute('drop table clienteTeru')

	def __str__(self):
		s = ""
		for query in self.c.execute("SELECT * FROM clienteTeru"):
			s += str(ClienteTeru(query)) + "\n"
		return s

	def __iter__(self):
		for query in self.c.execute("SELECT * FROM clienteTeru "):
			yield ClienteTeru(query)