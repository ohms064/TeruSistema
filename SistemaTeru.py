import datetime
import re

class MainSystem():
	def __init__(self, spreadsheet="reportes.csv"):
		self.spreadsheet = spreadsheet
		fecha = datetime.datetime.now()
		self.dia = str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year)
		with open("Comandas\\" + self.dia + ".csv", "a+") as arch:
			if (arch.tell() == 0):
				arch.write("hora,#Clientes,total,propina,total + propina,dineroRecibido,cambio")

	def nuevaComanda(self, numClientes, total, dineroRecibido, propina=0):
		self.error = False
		try:
			self.comanda = Comanda(int(numClientes), int(total), int(dineroRecibido), int(propina))
		except ValueError:
			self.error = True

	def nuevaPropina(self, propina):
		self.comanda.propina = int(propina)

	def commitComanda(self):
		temp = str(datetime.datetime.now().time())
		with open("Comandas\\" + self.dia + ".csv", "a") as arch:
			arch.write("\n" + temp[:temp.index(".")] + "," + str(self.comanda))

	def calculoComanda(self, con, string=False):
		total = sum(con)
		if string:
			return "Total: " + str(total) + "\nPropina Sugerida: " + str(int(total * 0.1)) + "\nTotal Sugerido: " + str(int(total * 1.1))
		return {"Total":str(total), "Propina":str(int(total*0.1)), "Sugerido": str(int(total * 1.1))}

	def cierreDeCaja(self, dineroCaja, gastos, nomina, dia=None):
		r = re.compile("[0-9][0-9]-")
		ventas = 0
		totalClientes = 0
		totalPropina = 0
		totalVentasPropina = 0
		if dia == "":
			dia = self.dia
		if gastos == "":
			gastos = 0
		if nomina == "":
			nomina = 0
		with open("Comandas\\" + self.dia + ".csv", "r") as arch:
			for line in arch.read():
				line = line.split(",")
				totalClientes += int(line[1])
				ventas += int(line[2])
				totalPropina += int(line[3])
				totalVentasPropina += int(line[4])


	def __bool__(self):
		return self.error

class Comanda(object):
	"""
	TODO:
		Eventualmente sería bueno agregarle consumo para que se puedan tener varias comandas al mismo tiempo	
	"""
	def __init__(self, numClientes, total, dineroRecibido, propina):
		self.numClientes = numClientes
		self.total = total
		self.propina = propina
		self.dineroRecibido = dineroRecibido

	def agregarPropina(self, propina=0):
		self.propina += propina

	def pago(self, dineroRecibido):
		self.dineroRecibido = dineroRecibido
		return self.total - self.dineroRecibido

	def cobro(self):
		return "Num. Clientes: " + str(self.numClientes) + "\nTotal: " + str(self.total) + "\nPropina: " + str(self.propina) +\
		 "\nTotal con Propina: " + str(self.total + self.propina) + "\nDinero Recibido: " + str(self.dineroRecibido) +\
		 "\nCambio: " + str(self.dineroRecibido - self.propina - self.total)

	def __str__(self):
		""" Formato: #Clientes, total, propina, total + propina, dineroRecibido, cambio """
		return str(self.numClientes) + "," + str(self.total) + "," + \
		 str(self.propina) + "," + str(self.propina + self.total)  + "," + \
		 str(self.dineroRecibido) + "," + str(self.dineroRecibido + self.propina - self.total)
