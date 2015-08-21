import tkinter as tk
import SistemaTeru

class MainGUI(tk.Frame):
	"""docstring for MainGUI"""
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.master.title("Teru Sistema")
		self.master.geometry("400x300")
		self.pack()
		self.createWidgets()
		self.sistema = SistemaTeru.MainSystem()

	def createWidgets(self):
		etiquetas = dict()
		self.texto = dict()
		self.strVar = dict()

		self.strVar["Clientes"] = tk.StringVar()
		self.strVar["Recibido"] = tk.StringVar()
		self.strVar["Propina"] = tk.StringVar()
		self.strVar["Total"] = tk.StringVar()

		etiquetas["Clientes"] = tk.Label(self.master, text="Clientes:").place(x=50, y=10)
		self.texto["Clientes"] = tk.Entry(self.master, textvariable=self.strVar["Clientes"]).place(x=110, y=10)

		etiquetas["Propina"] = tk.Label(self.master, text="Propina:").place(x=50, y=30)
		self.texto["Propina"] = tk.Entry(self.master, textvariable=self.strVar["Propina"]).place(x=110, y=30)

		etiquetas["Total"] = tk.Label(self.master, text="Total:").place(x=65, y=50)
		self.texto["Total"] = tk.Entry(self.master, textvariable=self.strVar["Total"]).place(x=110, y=50)

		etiquetas["Recibido"] = tk.Label(self.master, text="Dinero recibido:").place(x=10, y=70)
		self.texto["Recibido"] = tk.Entry(self.master, textvariable=self.strVar["Recibido"]).place(x=110, y=70)

		etiquetas["Consumo"] = tk.Label(self.master, text="Consumo:").place(x=40, y=130)
		self.texto["Consumo"] = tk.Text(self.master, width=24, height=5).place(x=110, y=130)
		butCalcular = tk.Button(self.master, text="Sumar", command=self.consumo).place(x=260, y=220)

		butAceptar = tk.Button(self.master, text="Aceptar", command=self.callSystem).place(x=185,y=95)
		butBorrar = tk.Button(self.master, text="Borrar", command=self.clearAll).place(x=125,y=95)

		print(type(self.texto["Consumo"]))

	def callSystem(self):
		if self.strVar["Propina"].get() == "":
			self.strVar["Propina"].set("0")
		self.sistema.nuevaComanda(self.strVar["Clientes"].get(), self.strVar["Total"].get(), self.strVar["Recibido"].get(), self.strVar["Propina"].get())
		newWindow = tk.Toplevel(self)
		newWindow.wm_title("Comanda")
		newWindow.geometry("250x180")
		recibo = tk.Label(newWindow, text=self.sistema.comanda.cobro()).place(x=60,y=10)
		butCommit = tk.Button(newWindow, text="Aceptar"). place(x=100,y=120)

	def clearAll(self):
		for i in self.strVar.keys():
			self.strVar[i].set("")
		self.texto["Consumo"].delete()

	def consumo(self):
		print(type(self.texto["Consumo"]))
		print(self.texto["Consumo"].get())


root = tk.Tk()
app = MainGUI(master=root)
app.mainloop()