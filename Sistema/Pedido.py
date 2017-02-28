
class Pedido(object):
	"""
	Clase usada durante la estancia del cliente para que se vayan agregando platillos a su orden
	"""
	def __init__(self):
		self.orden = list()

	def obtenerTotal(self):
		total = 0
		for i in orden:
			total += i.precio
		return total

	def agregar(self, platillo):
		self.orden.append(platillo)

	def __float__(self):
		return ObtenerTotal()

class Platillo(object):
	"""
	Clase ocupada para almacenar información de los platillos
	"""
	def __init__(self, nombre, precio):
		self.nombre = nombre
		self.precio = precio

	def __str__(self):
		return "{}, ${}".format(nombre, precio)