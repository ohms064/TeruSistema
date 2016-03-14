﻿import datetime
import sqlite3
import json

mes = ["?","Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto", "Septiembre","Octubre","Noviembre","Diciembre"]

class MainSystem():
	def __init__(self):
		fecha = datetime.datetime.now()
		self.dia = str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year)
		print(self.dia)
		self.reporteCadena = ""
		self.dineroCaja = ""
		with open("Comandas\\" + self.dia + ".csv", "a+") as arch:
			if (arch.tell() == 0):
				arch.write("hora,#Clientes,total,propina,total + propina,dineroRecibido,cambio")

	def nuevaComanda(self, numClientes, total, dineroRecibido, propina=0, tarjeta=False):
		"""
		Se agrega una nueva transacción.
		In:
		numCleintes: Número de cleintes en la mesa.
		total: El total del consumo
		dineroRecibido: Cuanto dinero se recibió
		propina(opcional): Cuanto se agregó de propina, esta propina se guarda en caja.
		tarjeta(opcional): Si el pago fué con tarjeta.
		"""
		self.error = False
		try:
			if tarjeta:
				dineroRecibido="0"
			self.comanda = Comanda(int(numClientes), int(total), int(dineroRecibido), int(propina), tarjeta)
		except ValueError:
			self.error = True

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
		"""
		temp = str(datetime.datetime.now().time())
		with open("Comandas\\" + self.dia + ".csv", "a") as arch:
			arch.write("\n" + temp[:temp.index(".")] + "," + str(self.comanda))

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
		 
class Comanda(object):
	"""
	TODO:
		Eventualmente sería bueno agregarle consumo para que se puedan tener varias comandas al mismo tiempo	
	"""
	def __init__(self, numClientes, total, dineroRecibido, propina, tarjeta=False):
		self.numClientes = numClientes
		self.total = total
		self.propina = propina
		self.dineroRecibido = dineroRecibido
		self.tarjeta = tarjeta

	def agregarPropina(self, propina=0):
		self.propina += propina

	def cobro(self):
		if self.tarjeta:
			return "Num. Clientes: " + str(self.numClientes) + "\nTotal: " + str(self.total) + "\nPropina: " + str(self.propina) +\
		 	"\nTotal con Propina: " + str(self.total + self.propina) + "\nPAGO CON TARJETA"
		return "Num. Clientes: " + str(self.numClientes) + "\nTotal: " + str(self.total) + "\nPropina: " + str(self.propina) +\
		 "\nTotal con Propina: " + str(self.total + self.propina) + "\nDinero Recibido: " + str(self.dineroRecibido) +\
		 "\nCambio: " + str(self.dineroRecibido - self.propina - self.total)

	def __str__(self):
		""" Formato: #Clientes, total, propina, total + propina, dineroRecibido, cambio """
		if self.tarjeta:
			return str(self.numClientes) + "," + str(self.total) + "," + \
		 str(self.propina) + "," + str(self.propina + self.total)  + "," + \
		 "TARJETA" + ",TARJETA" 

		return str(self.numClientes) + "," + str(self.total) + "," + \
		 str(self.propina) + "," + str(self.propina + self.total)  + "," + \
		 str(self.dineroRecibido) + "," + str(self.dineroRecibido - self.propina - self.total)

class ClienteTeru:
	def __init__(self):
		self.conexion = sqlite3.connect('Datos\\clientes.db')
		self.c = self.conexion.cursor()
		try:
			self.c.execute('''CREATE TABLE cleintes\
				( id INTEGER PRIMARY KEY, nombre VARCHAR, consumo REAL, visitas, INTEGER, , ultimaVisita VARCHAR, correo VARCHAR, nick VARCHAR)''')
			#Permite ejecutar sentencias sql en triples comillas
			#PRIMARY KEY ya crea de forma consecutiva los valores por default
		except:
			print ("Saltandose la creacion de la tabla por que ya existe")
	
	def insertar(self, nombre, consumo=0, visitas=0, ultimaVisita="0/0/0",correo="", nick=""):
		self.c.execute('''INSERT INTO clientes(nombre,consumo,visitas,ultimaVisita,correo)\
			VALUES('%s',%f,%f,'%s',%s)'''%(nombre, consumo, visitas, ultimaVisita, correo,nick))

	def confirmar(self):
		self.conexion.commit()

	def rewind(self):
		self.c.rollback()

	def buscarID(self,ide):
		return self.c.execute('''SELECT * FROM clientes WHERE id=%f'''%(ide)).fetchone()

	def buscarNombre(self, nombre):
		return self.c.execute('''SELECT * FROM clientes WHERE nombre=%s'''%(nombre)).fetchone()

	def buscarNick(self, nombre):
		return self.c.execute('''SELECT * FROM clientes WHERE nick=%s'''%(nick)).fetchone()

	def cerrar(self):
		self.conexion.close()

	def numClientes(self):
		return self.c.lastrowid()

if __name__ == '__main__':
	print("Porfavor abir TeruGUI")
	sistema = MainSystem()
	sistema.cierreDeCaja("1234", "12", "2", "20")
