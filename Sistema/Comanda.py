class Comanda(object):
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
		""" Formato: #Clientes, total, propina, total + propina, idCliente, nick, dineroRecibido, cambio"""
		if self.cliente:
			if self.tarjeta:
				return str(self.numClientes) + "," + str(self.total) + "," + \
			 str(self.propina) + "," + str(self.propina + self.total)  + "," + \
			 str(self.cliente.id) + "," + str(self.cliente.nick) + ",TARJETA,TARJETA"

			return str(self.numClientes) + "," + str(self.total) + "," + \
			 str(self.propina) + "," + str(self.propina + self.total)  + "," + \
			 str(self.dineroRecibido) + "," + str(self.dineroRecibido - self.propina - self.total)\
			  + "," + str(self.cliente.id) + "," + str(self.cliente.nick)
		else:
			if self.tarjeta:
				return str(self.numClientes) + "," + str(self.total) + "," + \
			 str(self.propina) + "," + str(self.propina + self.total)  + ",,," + \
			 "TARJETA,TARJETA"

			return str(self.numClientes) + "," + str(self.total) + "," + \
			 str(self.propina) + "," + str(self.propina + self.total)  + ",,," + \
			 str(self.dineroRecibido) + "," + str(self.dineroRecibido - self.propina - self.total)