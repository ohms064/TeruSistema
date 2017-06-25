from Datos.Platillos import TeruPlugin
from Sistema.CustomTK import UserForm
import copy
class Bebida(TeruPlugin.TeruPlugin):

	def configurationFileName(self):
		return "bebidas.json"

	def updatePedido(self, pedido, results, platillo):

		platilloCopy = copy.copy(platillo)
		platilloCopy.nombre += " {}".format(results["Extras"])
		try:
			platilloCopy.extra = int(results["Costo Extra"])
			platilloCopy.precio += platilloCopy.extra
		except:
			pass
		if results["Lychee Pops"]:
			platilloCopy.precio += self.lycheePrecio
			platilloCopy.nombre += " Lychee"
		if results["Frío"]:			
			platilloCopy.nombre += " Frío"
		return pedido.agregar(platilloCopy, int(results["Cantidad"]), byString=True)

	def createWindow(self, master, padre, done):
		return UserForm(master, done=done, padre=padre, keyLabels=self.configuration["keyLabels"], checkBox=self.configuration["checks"]\
			, choices=self.configuration["choices"])

	def fromSistema(self, sistema):
		"""
		Método donde se recibe el sistema de teru teru, 
		aquí se deberían obtener los datos necesarios para usarse en updatePedido o al crear la ventana
		"""
		self.lycheePrecio = 10
		try:
			lychee = sistema.platillosDB.buscarNombre("Pops lychee")
			self.lycheePrecio = int(lychee.precio)
		except:
			print("No se encontró PopsLychee en la base de datos, obteniendo de bebidas.json")
			self.lycheePrecio = int(self.configuration["Lychee Fallback"] )

		pass