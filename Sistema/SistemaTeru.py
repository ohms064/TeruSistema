import sqlite3
import datetime
import json
import os
from Sistema.Pedido import *
from Sistema.Comanda import *
from Sistema.Clientes import *

class MainSystem():
	def __init__(self):
		self.mes = ["?","Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto", "Septiembre","Octubre","Noviembre","Diciembre"]
		fecha = datetime.datetime.now()
		self.dia = str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year)
		self.reporteCadena = ""
		self.dineroCaja = ""
		os.makedirs("Datos", exist_ok=True)

		self.beginDB()

		with open("Comandas\\" + self.dia + ".csv", "a+") as arch:
			if (arch.tell() == 0):
				arch.write("hora,#Clientes,total,propina,total + propina,idCliente, nickCliente,dineroRecibido,cambio")
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
				self.conf = {"fecha" : self.dia, "promoVisitas" : 5, "visitas" : 0, "firstRun": True, "Categorias Platillo": []}
				json.dump(self.conf, archConf, indent=3)
		except Exception as err:
			self.escribirError(err)
			self.conf = {"fecha" : self.dia, "promoVisitas" : 5, "visitas" : 0, "firstRun": True, "Categorias Platillo": []}
		finally:
			print(self.conf)

	def escribirError(self, err):
		with open("error", "a") as archError:
			arcError.write("\nError {}\n\t".format(self.dia))
			archError.write(str(err))

	def nuevaComanda(self, numClientes, total, dineroRecibido, propina=0, tarjeta=False, idCliente=""):
		"""
		Se crea una nueva transacción.
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
			comanda = Comanda(int(numClientes), int(total), int(dineroRecibido), int(propina), tarjeta, cliente)
			return comanda

		except ValueError:
			self.error = True
			return None

	def llamarCliente(self, id):
		pass

	def beginDB(self):
		self.conexion = sqlite3.connect('Datos\\Teru.db')
		self.conexion.execute("PRAGMA journal_mode=WAL")
		self.clientesDB = ClienteDB(self.conexion)
		self.platillosDB = PlatilloDB(self.conexion)

	def nuevaPropina(self, propina):
		"""
		Se agrega propina a la camanda.
		In:
		propina: Valor de la propina actual.
		"""
		self.comanda.propina = int(propina)

	def commitComanda(self, comanda):
		"""
		Se guarda la información de la comanda.
		TODO:
		Comanda deberá convertirse en una tabla para una base de datos y esta función ya no estará en el MainSystem
		sino que en una clase llamada ComandaDB. Por lo mientras se tendrá ésto así.
		"""
		temp = str(datetime.datetime.now().time())
		with open("Comandas\\" + self.dia + ".csv", "a") as arch:
			arch.write("\n" + temp[:temp.index(".")] + "," + str(comanda))
		if comanda.cliente:
			self.clientesDB.incVisitas(comanda.cliente.id)
			self.clientesDB.incConsumo(comanda.cliente.id, comanda.total)
			self.clientesDB.actualizarUltimaVisita(comanda.cliente.id, self.dia)
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
			with open("Reportes\\Reporte-" + self.mes[int(diaFunc[1])] + "_" + diaFunc[2] + ".csv","a") as reporte:
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
		self.conexion.close()
		with open("Datos\\conf.json", "w") as archConf:
			self.conf["tutorialInicio"] = False
			json.dump(self.conf, archConf, indent=3)

if __name__ == '__main__':
	print("Porfavor abir TeruGUI")