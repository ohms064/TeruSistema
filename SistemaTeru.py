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
		print("commit")
		temp = str(datetime.datetime.now().time())
		with open("Comandas\\" + self.dia + ".csv", "a") as arch:
			arch.write("\n" + temp[:temp.index(".")] + "," + str(self.coamnda))

	def calculoComanda(self, con):
		total = sum(con)
		return "Total: " + str(total) + "\nPropina Sugerida: " + str(int(total * 0.1)) +\
		 "\nTotal Sugerido: " + str(int(total * 1.1))

	def cierreDeCaja(self, dineroCaja, dia=None):
		if dia is None:
			dia = self.dia
		with open("Comandas\\" + self.dia + ".csv", "r") as arch:
			for line in arch.read():
				line = line.split(",")

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
