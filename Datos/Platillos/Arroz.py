from Datos.Platillos import TeruPlugin
import copy
class Arroz(TeruPlugin.TeruPlugin):

	def updatePedido(self, pedido, results, platillo):

		platilloCopy = copy.copy(platillo)
		platilloCopy.nombre += " {} {}".format(results["Ingrediente"],results["Extras"])
		try:
			platilloCopy.extra = int(results["Costo Extra"])
			platilloCopy.precio += platilloCopy.extra
		except:
			pass
		return pedido.agregar(platilloCopy, int(results["Cantidad"]), byString=True)