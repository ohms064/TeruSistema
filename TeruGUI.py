import tkinter as tk

class MainGUI(tk.Frame):
	"""docstring for MainGUI"""
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.master.title("Teru Sistema")
		self.pack()
		self.createWidgets()

	def createWidgets(self):
		etiquetas = dict()
		etiquetas["Clientes"] = tk.Label(self, text="Clientes:")
		etiquetas["Recibido"] = tk.Label(self, text="Dinero recibido:")
		etiquetas["Propina"] = tk.Label(self, text="Propina:")
		etiquetas["Consumo"] = tk.Label(self, text="Consumo:")
