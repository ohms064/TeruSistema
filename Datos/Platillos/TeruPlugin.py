import importlib
import json
from tkinter import Frame, BooleanVar, Canvas, Scrollbar
from Sistema.CustomTK import UserForm
import copy

def loadPlugin(fileName, package=None):
	mod = importlib.import_module(fileName, package)
	plugin = getattr(mod, fileName)
	return plugin()

class TeruPlugin:
	def __init__(self, path="Datos/Platillos/"):
		fullPath = path + self.configurationFileName()
		self.loadConfiguration(fullPath)

	def loadConfiguration(self, conf="Datos/Platillos/general.json"):
		try:
			with open(conf, "r", encoding="utf8") as confFile:
				self.configuration = json.load(confFile)
		except:
			#No configuration file
			return
		self.size = ""
		if "size" in self.configuration:
			self.size = self.configuration["size"]

	def configurationFileName(self):
		"""
		Retorna el nombre del archivo de configuración a usar.
		"""
		return "general.json"

	def updatePedido(self, pedido, results, platillo):
		"""
		De los datos obtenidos de createWindowWait se modifica el valor del pedido conforme sea necesario.
		Aquí se debería agregar el platillo a la orden y se debe retornar el índice del valor modificado.
		"""
		platilloCopy = copy.copy(platillo)
		platilloCopy.nombre += " " + results["Extras"]
		print(results["Costo Extra"])
		try:
			platilloCopy.precio += int(results["Costo Extra"])
		except:
			pass
		return pedido.agregar(platilloCopy, int(results["Cantidad"]), byString=True)

	def createWindowWait(self, master, padre, wait=True):
		"""
		Método que debe crear una ventana y devolver los valores necesarios obtenidos de dicha ventana.
		"""
		done = BooleanVar()
		window = UserForm(master, done=done, padre=padre, keyLabels=self.configuration["keyLabels"], choices=self.configuration["choices"])
		self.size+="+{}+{}".format(padre.winfo_rootx(), padre.winfo_rooty())

		master.geometry(self.size)
		if wait:
			master.wait_variable(done)
		return window.formValues

	def withPlatillo(self, platillo):
		"""
		Método donde se indica que platillo de ocupará para el plugin.
		Aquí se puede usar la información para llenar datos de la ventana
		"""
		self.platillo = platillo
