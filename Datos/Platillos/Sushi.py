from Datos.Platillos import TeruPlugin
import copy
class Sushi(TeruPlugin.TeruPlugin):
	def configurationFileName(self):
		return "sushi.json"

	def updatePedido(self, pedido, results, platillo):

		platilloCopy = copy.copy(platillo)
		platilloCopy.nombre += " {} {}".format(results["Ingrediente"],results["Extras"])
		return pedido.agregar(platilloCopy, int(results["Cantidad"]), byString=True)