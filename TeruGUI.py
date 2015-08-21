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
		self.strVar = dict()

		self.strVar["Clientes"] = tk.StringVar()
		self.strVar["Recibido"] = tk.StringVar()
		self.strVar["Propina"] = tk.StringVar()
		self.strVar["Total"] = tk.StringVar()

		tk.Label(self.master, text="Clientes:").place(x=50, y=10)
		tk.Entry(self.master, textvariable=self.strVar["Clientes"]).place(x=110, y=10)

		tk.Label(self.master, text="Propina:").place(x=50, y=30)
		tk.Entry(self.master, textvariable=self.strVar["Propina"]).place(x=110, y=30)

		tk.Label(self.master, text="Total:").place(x=65, y=50)
		tk.Entry(self.master, textvariable=self.strVar["Total"]).place(x=110, y=50)

		tk.Label(self.master, text="Dinero recibido:").place(x=10, y=70)
		tk.Entry(self.master, textvariable=self.strVar["Recibido"]).place(x=110, y=70)

		tk.Button(self.master, text="Aceptar", command=self.callSystem).place(x=185,y=95)
		tk.Button(self.master, text="Borrar", command=self.clearComanda).place(x=125,y=95)

		tk.Label(self.master, text="Consumo:").place(x=40, y=130)
		self.textoConsumo = tk.Text(self.master, width=24, height=5)
		self.textoConsumo.place(x=110, y=130)
		tk.Button(self.master, text="Sumar", command=self.consumo).place(x=260, y=220)
		tk.Button(self.master, text="Borrar", command=self.clearConsumo).place(x=200,y=220)


	def callSystem(self):
		if self.strVar["Propina"].get() == "":
			self.strVar["Propina"].set("0")
		
		self.sistema.nuevaComanda(self.strVar["Clientes"].get(), self.strVar["Total"].get(), self.strVar["Recibido"].get(), self.strVar["Propina"].get())
		self.resultWindow = tk.Toplevel(self)
		self.resultWindow.wm_title("Comanda")
		self.resultWindow.geometry("250x180")
		if self.sistema:
			tk.Label(self.resultWindow, text="Error!").place(x=60,y=10)	
			tk.Button(self.resultWindow, text="Aceptar", command=self.resultWindow.destroy). place(x=100,y=120)
		else:
			tk.Label(self.resultWindow, text=self.sistema.comanda.cobro()).place(x=60,y=10)
			tk.Button(self.resultWindow, text="Aceptar", command=self.aceptarComanda). place(x=100,y=120)

	def clearComanda(self):
		for i in self.strVar.keys():
			self.strVar[i].set("")
		
	def clearConsumo(self):
		self.textoConsumo.delete('1.0', '2.0')

	def consumo(self):
		error = False
		cons = self.textoConsumo.get("1.0","end").split()
		try:
			cons = [int(x) for x in cons]
			cons = self.sistema.calculoComanda(cons)
		except ValueError:
			error = True
			cons = "Error!"
		self.consWindow = tk.Toplevel(self)
		self.consWindow.wm_title("Resultado")
		self.consWindow.geometry("150x150")
		tk.Label(self.consWindow, text=cons).place(x=20, y=20)
		if error:
			tk.Button(self.consWindow, text="Aceptar", command=self.consWindow.destroy).place(x=50,y=90)
		else:
			tk.Button(self.consWindow, text="Aceptar", command=self.aceptarConsumo).place(x=50,y=90)

	def aceptarConsumo(self):
		self.consWindow.destroy()
		self.clearConsumo()

	def aceptarComanda(self):
		self.sistema.commitComanda()
		self.resultWindow.destroy()
		self.clearComanda()

	

root = tk.Tk()
app = MainGUI(master=root)
app.mainloop()