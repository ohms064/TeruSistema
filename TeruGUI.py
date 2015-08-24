import tkinter as tk
import SistemaTeru

class Instanciador(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.master.title("Teru Sistema")
		self.master.geometry("170x75")
		self.pack()
		self.contador = 0
		self.sistema = SistemaTeru.MainSystem()
		self.textContador = tk.StringVar()
		self.textContador.set("Mesas: " + str(self.contador))
		self.createWidgets()

	def createWidgets(self):
		self.folioLabel = tk.Label(self.master, textvariable=self.textContador).place(x=60, y=10)
		tk.Button(self.master, text="Nueva Mesa", command=self.nuevaMesa).place(x=50,y=40)
		tk.Button(self.master, text="Cierre de caja", command=self.confirmacionCierre).place(x=45,y=80)

	def nuevaMesa(self):
		self.contador += 1
		self.textContador.set("Mesas: " + str(self.contador))
		MainGUI(self.sistema, self.contador, tk.Toplevel(self))


	def confirmacionCierre(self):
		self.cierreWindow = tk.Toplevel(self)
		self.cierreWindow.wm_title("Cierre")
		self.cierreWindow.geometry("280x190")
		tk.Label(self.cierreWindow, text="Fecha (dd-mm-año):").place(x=10,y=10)
		tk.Entry(self.cierreWindow, textvariable=self.strVar["Dia"]).place(x=130, y=10)
		tk.Label(self.cierreWindow, text="Nota: Dejar vacío si se quiere el día de hoy").place(x=30,y=30)
		tk.Label(self.cierreWindow, text="Dinero en caja:").place(x=45,y=60)
		tk.Entry(self.cierreWindow, textvariable=self.strVar["Dinero"]).place(x=130, y=60)
		tk.Label(self.cierreWindow, text="Gastos:").place(x=85,y=90)
		tk.Entry(self.cierreWindow, textvariable=self.strVar["Gastos"]).place(x=130, y=90)
		tk.Label(self.cierreWindow, text="Nómina(Total):").place(x=45,y=120)
		tk.Entry(self.cierreWindow, textvariable=self.strVar["Nomina"]).place(x=130, y=120)

		tk.Button(self.cierreWindow, text="Aceptar").place(x=100,y=150)

	def cerrarCaja(self):
		if self.strVar["Dinero"].get().isdigit():
			try:
				self.sistema.cierreDeCaja(self.strVar["Dinero"], )
			except:
				pass
		

class MainGUI(tk.Frame):
	"""docstring for MainGUI"""
	def __init__(self, sistema=SistemaTeru.MainSystem(), folio="0", master=None):
		tk.Frame.__init__(self, master)
		self.folio = folio
		self.master.title("Teru Sistema " + str(self.folio))
		self.master.geometry("400x270")
		self.pack()
		self.createWidgets()
		self.sistema = sistema

	def createWidgets(self):
		self.strVar = dict()

		self.strVar["Dia"] = tk.StringVar()
		self.strVar["Clientes"] = tk.StringVar()
		self.strVar["Recibido"] = tk.StringVar()
		self.strVar["Propina"] = tk.StringVar()
		self.strVar["Total"] = tk.StringVar()
		self.strVar["Dinero"] = tk.StringVar()
		self.strVar["Gastos"] = tk.StringVar()
		self.strVar["Nomina"] = tk.StringVar()

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
		tk.Button(self.master, text="Añadir", command=self.añadir).place(x=260, y=220)
		tk.Button(self.master, text="Sumar", command=self.consumo).place(x=200, y=220)
		tk.Button(self.master, text="Borrar", command=self.clearConsumo).place(x=140,y=220)

	def callSystem(self):
		if self.strVar["Propina"].get() == "":
			self.strVar["Propina"].set("0")
		self.master.withdraw()
		self.sistema.nuevaComanda(self.strVar["Clientes"].get(), self.strVar["Total"].get(), self.strVar["Recibido"].get(), self.strVar["Propina"].get())
		self.resultWindow = tk.Toplevel(self)
		self.resultWindow.wm_title("Comanda")
		self.resultWindow.geometry("250x180")
		if self.sistema:
			tk.Label(self.resultWindow, text="Error!").place(x=60,y=10)	
			tk.Button(self.resultWindow, text="Aceptar", command=self.show). place(x=100,y=120)
		else:
			tk.Label(self.resultWindow, text=self.sistema.comanda.cobro()).place(x=60,y=10)
			tk.Button(self.resultWindow, text="Cancelar", command=self.show). place(x=50,y=120)
			tk.Button(self.resultWindow, text="Aceptar", command=self.aceptarComanda). place(x=150,y=120)

	def clearComanda(self):
		for i in self.strVar.keys():
			self.strVar[i].set("")
		
	def clearConsumo(self):
		self.textoConsumo.delete('1.0', '2.0')

	def consumo(self):
		cons = self.textoConsumo.get("1.0","end").split()
		try:
			cons = [int(x) for x in cons]
			cons = self.sistema.calculoComanda(cons)
			self.strVar["Total"].set(cons["Total"])
			self.strVar["Propina"].set(cons["Propina"])
		except ValueError:
			self.consWindow = tk.Toplevel(self)
			self.consWindow.wm_title("Resultado")
			self.consWindow.geometry("200x150")
			tk.Label(self.consWindow, text="Error!").place(x=30, y=20)
			tk.Button(self.consWindow, text="Aceptar", command=self.consWindow.destroy).place(x=75,y=90)
		
	def añadir(self):
		cons = self.textoConsumo.get("1.0","end").split()
		try:
			cons = [int(x) for x in cons]
			if self.strVar["Total"].get() == "":
				cons = self.sistema.calculoComanda(cons)
			else:
				cons = self.sistema.calculoComanda(cons + [int(self.strVar["Total"].get())])
			self.strVar["Total"].set(cons["Total"])
			self.strVar["Propina"].set(cons["Propina"])
		except ValueError:
			self.consWindow = tk.Toplevel(self)
			self.consWindow.wm_title("Resultado")
			self.consWindow.geometry("200x150")
			tk.Label(self.consWindow, text="Error!").place(x=30, y=20)
			tk.Button(self.consWindow, text="Aceptar", command=self.consWindow.destroy).place(x=75,y=90)

	def aceptarConsumo(self):
		self.consWindow.destroy()
		self.master.destroy()
		self.clearConsumo()

	def aceptarComanda(self):
		self.sistema.commitComanda()
		self.resultWindow.destroy()
		self.clearComanda()

	def show(self):
		self.resultWindow.destroy()
		self.master.update()
		self.master.deiconify()

if __name__ == '__main__':
	root = tk.Tk()
	app = Instanciador(master=root)
	app.mainloop()