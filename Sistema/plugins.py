import importlib
import json
from tkinter import Frame
from Sistema.CustomTK import UserForm

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
			with open(conf, "r") as confFile:
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

	def modifyPlatillo(self, platillo, value):
		"""
		De los datos obtenidos de createWindowWait se modifica el valor de platillo conforme sea necesario
		"""
		platillo[1] = value["Cantidad"]
		return platillo

	def createWindowWait(self, master, padre, wait):
		"""
		Método que debe crear una ventana y devolver los valores necesarios obtenidos de dicha ventana.
		"""
		frame = Frame(master=master)
		master.geometry(self.size)
		window = UserForm(master=frame, done=wait, padre=padre, self.configuration["keyLabels"], choices=self.configuration["choices"])
		master.wait_variable(wait)
		return window.formValues



