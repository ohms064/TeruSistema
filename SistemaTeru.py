import datetime
import sqlite3
import json
import os

mes = ["?","Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto", "Septiembre","Octubre","Noviembre","Diciembre"]

class MainSystem():
	def __init__(self):
		fecha = datetime.datetime.now()
		self.dia = str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year)
		self.reporteCadena = ""
		self.dineroCaja = ""
		os.makedirs("Datos", exist_ok=True)
		self.clientesDB = ClienteDB()
		with open("Comandas\\" + self.dia + ".csv", "a+") as arch:
			if (arch.tell() == 0):
				arch.write("hora,#Clientes,total,propina,total + propina,dineroRecibido,cambio, idCliente")
		try:
			with open("Datos\\conf.json", "r") as archConf:
				self.conf = json.load(archConf)
				if self.conf["fecha"] != self.dia:#Si cambio la fecha
					self.conf["visitas"] = 0
					self.conf["fecha"] = self.dia	
					if self.conf["fecha"].split("-")[1] != self.dia.split("-")[1]:#Cambio de mes
						self.clientesDB.resetVisitas()
						self.clientesDB.resetConsumo()
					
		except (FileNotFoundError, ValueError) as err:
			with open("Datos\\conf.json", "w") as archConf:
				self.conf = {"fecha" : self.dia, "promoVisitas" : 5, "visitas" : 0, "firstRun": True}
				json.dump(self.conf, archConf, indent=3)
		except:
			with open("error", "w") as archError:
				archError.write(sys.exc_info()[0])
				self.conf = {"fecha" : self.dia, "promoVisitas" : 5, "visitas" : 0, "firstRun": True}
		finally:
			print(self.conf)

	def nuevaComanda(self, numClientes, total, dineroRecibido, propina=0, tarjeta=False, idCliente=""):
		"""
		Se agrega una nueva transacción.
		In:
		numCleintes: Número de cleintes en la mesa.
		total: El total del consumo
		dineroRecibido: Cuanto dinero se recibió
		propina(opcional): Cuanto se agregó de propina, esta propina se guarda en caja.
		tarjeta(opcional): Si el pago fué con tarjeta.
		idCliente(opcional): El id del cliente.
		"""
		self.error = False
		try:
			if tarjeta:
				dineroRecibido="0"
			cliente = self.clientesDB.buscarID(idCliente)
			self.comanda = Comanda(int(numClientes), int(total), int(dineroRecibido), int(propina), tarjeta, cliente)
		except ValueError:
			self.error = True

	def llamarCliente(self, id):
		pass

	def nuevaPropina(self, propina):
		"""
		Se agrega propina a la camanda.
		In:
		propina: Valor de la propina actual.
		"""
		self.comanda.propina = int(propina)

	def commitComanda(self):
		"""
		Se guarda la información de la comanda.
		TODO:
		Comanda deberá convertirse en una tabla para una base de datos y esta función ya no estará en el MainSystem
		sino que en una clase llamada ComandaDB. Por lo mientras se tendrá ésto así.
		"""
		temp = str(datetime.datetime.now().time())
		with open("Comandas\\" + self.dia + ".csv", "a") as arch:
			arch.write("\n" + temp[:temp.index(".")] + "," + str(self.comanda))
		if self.comanda.cliente:
			self.clientesDB.incVisitas(self.comanda.cliente.id)
			self.clientesDB.incConsumo(self.comanda.cliente.id, self.comanda.total)
			self.actualizarUltimaVisita(self.comanda.cliente.id, self.dia)
			self.clientesDB.confirmar()

	def calculoComanda(self, con, string=False):
		"""
		Se calcula el total de una comanda y se regresa los valores esperados.
		In:
		con: Lista con el consumo
		string: Si la salida es una cadena o diccionario.
		Out:
			Una cadena o diccionario con los totales, propinas y total con propina.
		"""
		total = sum(con)
		if string:
			return "Total: " + str(total) + "\nPropina Sugerida: " + str(int(total * 0.1)) + "\nTotal Sugerido: " + str(int(total * 1.1))
		return {"Total":str(total), "Propina":str(int(total*0.1)), "Sugerido": str(int(total * 1.1))}

	def cierreDeCaja(self, dineroCaja, dineroInicial, gastos="", nomina="", dia=""):
		"""
		Función que almacena la información de cierre de caja
		In:
		dineroCaja: Dinero que se encuentra en caja a la hora de cierre
		gastos (opcional): Dinero que se ha gastado durante el día.
		nomina (opcional): Dinero que se les pagó a los empleados
		dia (opcional): Dia del que se quiere hacer cierre de caja, en caso de no enviarse se tomará el actual.
		"""
		self.dineroCaja = int(dineroCaja)
		self.reporteCadena = ""
		totalClientes = 0
		ventasEfectivo = 0
		ventasTarjeta = 0
		
		self.totalPropinaEfectivo = 0
		self.totalPropinaTarjeta = 0
		totalVentasPropina = 0
		totalMesas = 0
		dineroInicial = int(dineroInicial)
		if dia == "":
			diaFunc = self.dia.split("-")
		else:
			diaFunc = dia
		diaFunc = [x.lstrip("0") for x in diaFunc]
		if gastos == "":
			gastos = 0
		else:
			gastos = int(gastos)

		if nomina == "":
			nomina = 0
		else:
			nomina = int(nomina)
		try:
			with open("Comandas\\" + str(diaFunc[0]) + "-" + str(diaFunc[1]) + "-" + str(diaFunc[2]) + ".csv", "r") as arch:
				#Leemos todos los datos recopilados del día.
				for line in arch:
					if not line.startswith("hora") and not (line + " ").isspace():
						line = line.split(",")
						totalMesas += 1
						totalClientes += int(line[1])
						if line[-1].rstrip("\n") == "TARJETA":
							ventasTarjeta += int(line[2])
							self.totalPropinaTarjeta += int(line[3])
						else:
							ventasEfectivo += int(line[2])
							self.totalPropinaEfectivo += int(line[3])
						totalVentasPropina += int(line[4])
		except FileNotFoundError:
			return "Archivo no encontrado " + str(diaFunc[0]) + "-" + str(diaFunc[1]) + "-" + str(diaFunc[2]) + ".csv"

		#El cálculo se hace con el dinero en caja después de haber entregado las propinas y la nómina
		neto = dineroInicial + ventasEfectivo - gastos - nomina - self.totalPropinaTarjeta
		diffDinero = self.dineroCaja - neto

		self.reporteCadena = str(diaFunc[0]) + "-" + str(diaFunc[1]) + "," + str(totalMesas) + "," + str(totalClientes) + "," +\
		str(dineroInicial) + "," + str(ventasEfectivo) + "," + str(ventasTarjeta + self.totalPropinaTarjeta) + "," + str(gastos) + "," +\
		str(nomina) + "," + str(neto) + "," + str(self.dineroCaja) + "," + str(diffDinero)
		return (self.reporteCadena, self.totalPropinaTarjeta + self.totalPropinaEfectivo)

	def commitCierre(self, llevo, dia=""):
		"""
		Se guarda el cierre en el archivo de reportes.
		In: 
		llevo: dinero que se saca de la caja para guardarse.
		dia (opcional): Dia del que se quiere hacer cierre de caja, en caso de no enviarse se tomará el actual.
		"""
		if dia == "":
			diaFunc = self.dia.split("-")
		else:
			diaFunc = dia
		diaFunc = [x.lstrip("0") for x in diaFunc]
		try:
			with open("Reportes\\Reporte-" + mes[int(diaFunc[1])] + "_" + diaFunc[2] + ".csv","a") as reporte:
				if reporte.tell() == 0:
					reporte.write("Dia,Total Mesas,Total Clientes,Caja,Cobro Efectivo,Terminal,Gastos,Sueldo,Neto,Dinero,Sobra/Falta,Llevo,Dejo,Propinas Efectivo, Propinas Tarjeta, Total Propinas\n")
				self.reporteCadena += "," + llevo + "," + str(int(self.dineroCaja) - int(llevo)) + "," + str(self.totalPropinaEfectivo) + "," + str(self.totalPropinaTarjeta) + "," + str(self.totalPropinaTarjeta + self.totalPropinaEfectivo) + "\n"
				reporte.write(self.reporteCadena)
		except PermissionError:
			print("Favor de cerrar el archivo del reporte")

	def __bool__(self):
		return self.error

	def getState(self):
		"""
		Nos retorna el estado actual del sistema.
		El orden es fecha, totalMesas, totalClientes, ventasEfectivo, ventasTerminal, propinasTotal.
		"""
		totalClientes = 0
		ventasEfectivo = 0
		ventasTarjeta = 0
		
		totalPropinaEfectivo = 0
		totalPropinaTarjeta = 0
		totalVentasPropina = 0
		totalMesas = 0
		diaFunc = self.dia.split("-")
		try:
			with open("Comandas\\" + str(diaFunc[0]) + "-" + str(diaFunc[1]) + "-" + str(diaFunc[2]) + ".csv", "r") as arch:
				#Leemos todos los datos recopilados del día.
				for line in arch:
					if not line.startswith("hora") and not (line + " ").isspace():
						line = line.split(",")
						totalMesas += 1
						totalClientes += int(line[1])
						if line[-1].rstrip("\n") == "TARJETA":
							ventasTarjeta += int(line[2])
							totalPropinaTarjeta += int(line[3])
						else:
							ventasEfectivo += int(line[2])
							totalPropinaEfectivo += int(line[3])
						totalVentasPropina += int(line[4])
		except FileNotFoundError:
			return "Archivo no encontrado " + str(diaFunc[0]) + "-" + str(diaFuncdiaFunc[1]) + "-" + str(diaFunc[2]) + ".csv"
		
		return "Fecha: " + (diaFunc[0]) + "-" + str(diaFunc[1]) + "\nTotal Mesas: " + str(totalMesas) + "\nTotal Clientes: " + str(totalClientes) + "\nVentas Efectivo: " +\
		 str(ventasEfectivo) + "\nVentas Terminal: " + str(ventasTarjeta + totalPropinaTarjeta) + "\nPropinas Efectivo : " + str(totalPropinaEfectivo) + "\nPropinas Tarjeta: " + str(totalPropinaTarjeta)
		 
	def __del__(self):
		self.clientesDB.cerrar()
		with open("Datos\\conf.json", "w") as archConf:
			self.conf["tutorialInicio"] = False
			json.dump(self.conf, archConf, indent=3)

class Comanda(object):
	"""
	TODO:
		Eventualmente sería bueno agregarle consumo para que se puedan tener varias comandas al mismo tiempo	
	"""
	def __init__(self, numClientes, total, dineroRecibido, propina, tarjeta=False, cliente=""):
		self.numClientes = numClientes
		self.total = total
		self.propina = propina
		self.dineroRecibido = dineroRecibido
		self.tarjeta = tarjeta
		self.cliente = cliente

	def agregarPropina(self, propina=0):
		self.propina += propina

	def cobro(self):
		if self.tarjeta:
			return "Num. Clientes: " + str(self.numClientes) + "\nTotal: " + str(self.total) + "\nPropina: " + str(self.propina) +\
		 	"\nTotal con Propina: " + str(self.total + self.propina) + "\nPAGO CON TARJETA\n" + self.cliente.beautifulString()
		return "Num. Clientes: " + str(self.numClientes) + "\nTotal: " + str(self.total) + "\nPropina: " + str(self.propina) +\
		 "\nTotal con Propina: " + str(self.total + self.propina) + "\nDinero Recibido: " + str(self.dineroRecibido) +\
		 "\nCambio: " + str(self.dineroRecibido - self.propina - self.total) + "\n" + self.cliente.beautifulString()

	def __str__(self):
		""" Formato: #Clientes, total, propina, total + propina, dineroRecibido, cambio, idCliente, nick """
		if self.tarjeta:
			return str(self.numClientes) + "," + str(self.total) + "," + \
		 str(self.propina) + "," + str(self.propina + self.total)  + "," + \
		 "TARJETA,TARJETA,"+ str(self.cliente.id) + "," + str(self.cliente.nick )

		return str(self.numClientes) + "," + str(self.total) + "," + \
		 str(self.propina) + "," + str(self.propina + self.total)  + "," + \
		 str(self.dineroRecibido) + "," + str(self.dineroRecibido - self.propina - self.total)\
		  + "," + str(self.cliente.id) + "," + str(self.cliente.nick)

class ClienteDB:
	def __init__(self):
		self.conexion = sqlite3.connect('Datos\\clientesTeru.db')
		self.c = self.conexion.cursor()
		
		self.c.execute("CREATE TABLE IF NOT EXISTS clientesTeru \
			( id INTEGER PRIMARY KEY, \
			nombre VARCHAR, \
			consumo REAL, \
			visitas INTEGER, \
			ultimaVisita VARCHAR, \
			correo VARCHAR, \
			nick VARCHAR, \
			fechaIngreso VARCHAR)")
	
	def insertar(self, nombre, consumo=0, correo="", nick="", ultimaVisita="0-0-0", visitas=1, fechaIngreso="0-0-0"):
		if ultimaVisita == "0-0-0":
			fecha = datetime.datetime.now()
			ultimaVisita = str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year)
		if fechaIngreso == "0-0-0":
			fecha = datetime.datetime.now()
			fechaIngreso = str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year)

		sql = "INSERT INTO clientesTeru(nombre, consumo, visitas, ultimaVisita, correo, nick, fechaIngreso) \
		VALUES ('{}', {}, {}, '{}', '{}', '{}', '{}')".format(nombre, consumo, visitas, ultimaVisita, correo, nick, fechaIngreso)
		self.c.execute(sql)

	def actualizar(self, identificador, nombre="", nick="", correo=""):
		"""
		Función para actualizar los datos de un cliente con un identificador.
		"""	
		if nombre == "" and nick == "" and correo == "":#Seguramente esto se puede mejorar usando **args
			return
		sql = "UPDATE clientesTeru SET "
		if nombre != "":
			sql += "nombre = '{}', ".format(nombre)
		if nick != "":
			sql += "nick = '{}', ".format(nick)
		if correo != "":
			sql += "correo = '{}', ".format(correo)
		sql = sql[0:-2] + " WHERE id={}".format(identificador)
		self.c.execute(sql)

	def borrar(self, identificador):
		self.c.execute("DELETE FROM clientesTeru WHERE id={}".format(identificador))

	def confirmar(self):
		self.conexion.commit()

	def rewind(self):
		self.c.rollback()

	def buscarID(self,ide):
		"""
		Busca en la tabla por ID y retorna el primer valor encontrado
		"""
		return ClienteTeru(self.c.execute("SELECT * FROM clientesTeru WHERE id='{}'".format(ide)).fetchone())

	def buscarNombre(self, nombre):
		"""
		Busca en la tabla por nombre y retorna el primer valor encontrado
		"""
		return ClienteTeru(self.c.execute("SELECT * FROM clientesTeru WHERE nombre='{}'".format(nombre)).fetchone())

	def buscarNick(self, nick):
		"""
		Busca en la tabla por nick y retorna el primer valor encontrado
		"""
		return ClienteTeru(self.c.execute("SELECT * FROM clientesTeru WHERE nick='{}'".format(nick)).fetchone())

	def resetVisitas(self):
		"""
		Resetea a todos los clientes su valor de visitas a 0. Esto para que se haga cada mes.
		"""
		self.c.execute(" UPDATE clientesTeru SET visitas = 0")

	def resetConsumo(self):
		"""
		Resetea a todos los clientes su valor de visitas a 0. Esto para que se haga cada mes.
		"""
		self.c.execute(" UPDATE clientesTeru SET consumo = 0")

	def incVisitas(self, identificador):
		"""
		Se incrementa el valor de las visitas por 1.
		"""
		self.c.execute(" UPDATE clientesTeru SET visitas = visitas + 1 WHERE id={}".format(identificador))

	def incConsumo(self, identificador, consumo):
		self.c.execute(" UPDATE clientesTeru SET consumo = consumo + {} WHERE id={}".format(consumo, identificador))	

	def actualizarUltimaVisita(self, identificador, fecha):
		self.c.execute(" UPDATE clientesTeru SET ultimaVisita = {} WHERE id={}".format(fecha, identificador))			

	def buscarCorreo(self, correo):
		"""
		Busca en la tabla por correo y retorna el primer valor encontrado
		"""
		return ClienteTeru(self.c.execute("SELECT * FROM clientesTeru WHERE correo='{}'".format(correo)).fetchone())

	def cerrar(self):
		self.conexion.close()

	def drop(self):
		self.c.execute('drop table clientesTeru')

	def __len__(self):
		return self.c.lastrowid

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.cerrar()

	def __str__(self):
		s = ""
		for query in self.c.execute("SELECT * FROM clientesTeru"):
			s += str(ClienteTeru(query)) + "\n"
		return s

	def __iter__(self):
		for query in self.c.execute("SELECT * FROM clientesTeru "):
			yield ClienteTeru(query)

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
		if self.id != "¡ERROR! No se encontró información":
			return "ID: " + str(self.id) + "\nNombre: " + str(self.nombre) + "\nVisitas: " + str(self.visitas) + "\nCorreo: " + str(self.correo) + "\nNick: " + str(self.nick)
		return ""

	def __str__(self):
		return str(self.id) + "," + str(self.nombre) + "," + str(self.consumo) + "," + str(self.visitas) + " ," + str(self.ultimaVisita) + "," + str(self.correo) + "," + str(self.nick)

	def __bool__(self):
		return self.id != "¡ERROR! No se encontró información"

if __name__ == '__main__':
	print("Porfavor abir TeruGUI")