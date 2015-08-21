import datetime

class MainSystem():
	def __init__(self, spreadsheet="reportes.csv"):
		self.spreadsheet = spreadsheet
		fecha = datetime.datetime.now()
		self.dia = str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year)
		with open("Comandas\\" + self.dia + ".csv", "a+") as arch:
			if (arch.tell() == 0):
				arch.write("hora,#Clientes,total,propina,total + propina,dineroRecibido,cambio")

	def nuevaComanda(self, numClientes, total, dineroRecibido, propina=0):
		self.comanda = Comanda(int(numClientes), int(total), int(dineroRecibido), int(propina))

	def nuevaPropina(self, propina):
		self.comanda.propina = int(propina)

	def commitComanda(self):
		print("commit")
		temp = str(datetime.datetime.now().time())
		with open("Comandas\\" + self.dia + ".csv", "a") as arch:
			arch.write("\n" + temp[:temp.index(".")] + "," + str(self.comanda))

	def consumo(self, con):
		total = sum(con)
		return "Total: " + str(total) + "Propina Sugerida: " + str(total * 0.1) +\
		 "Total Sugerido: " + str(total * 1.1)


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
		self.cambio = self.dineroRecibido - self.total

	def agregarPropina(self, propina=0):
		self.propina += propina

	def pago(self, dineroRecibido):
		self.dineroRecibido = dineroRecibido
		return self.total - self.dineroRecibido

	def cobro(self):
		return "Num. Clientes: " + self.numClientes + "\nTotal: " + str(self.total) + "\nPropina: " + str(self.propina) +\
		 " Total con Propina: " + str(self.total + self.propina) + "\nDinero Recibido: " + str(self.dineroRecibido) +\
		 "Cambio: " + str(self.cambio)

	def __str__(self):
		""" Formato: #Clientes, total, propina, total + propina, dineroRecibido, cambio """
		return str(self.numClientes) + "," + str(self.total) + "," + \
		 str(self.propina) + "," + str(self.propina + self.total)  + "," + \
		 str(self.dineroRecibido) + "," + str(self.cambio)
