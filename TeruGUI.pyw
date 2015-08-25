import tkinter as tk
import SistemaTeru

class Instanciador(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.master.title("Teru Sistema")
		self.master.geometry("170x120")
		self.pack()
		self.createWidgets()

	def createWidgets(self):
		self.contador = 0
		self.sistema = SistemaTeru.MainSystem()
		self.textContador = tk.StringVar()
		self.dinero = tk.StringVar()
		self.gastos = tk.StringVar()
		self.nomina = tk.StringVar()
		self.propina = tk.StringVar()
		self.dineroInicial = tk.StringVar()
		self.dia = tk.StringVar()
		self.textContador.set("Mesas: " + str(self.contador))
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
		self.cierreWindow.geometry("280x250")
		tk.Label(self.cierreWindow, text="Fecha (dd-mm-año):").place(x=10,y=10)
		tk.Entry(self.cierreWindow, textvariable=self.dia).place(x=130, y=10)
		tk.Label(self.cierreWindow, text="Nota: Dejar vacío si se quiere el día de hoy").place(x=30,y=30)
		tk.Label(self.cierreWindow, text="Dinero en caja:").place(x=45,y=60)
		tk.Entry(self.cierreWindow, textvariable=self.dinero).place(x=130, y=60)
		tk.Label(self.cierreWindow, text="Dinero Inicial:").place(x=50,y=90)
		tk.Entry(self.cierreWindow, textvariable=self.dineroInicial).place(x=130, y=90)
		tk.Label(self.cierreWindow, text="Gastos:").place(x=85,y=120)
		tk.Entry(self.cierreWindow, textvariable=self.gastos).place(x=130, y=120)
		tk.Label(self.cierreWindow, text="Nómina(Total):").place(x=45,y=150)
		tk.Entry(self.cierreWindow, textvariable=self.nomina).place(x=130, y=150)
		tk.Label(self.cierreWindow, text="Propina:").place(x=80,y=180)
		tk.Entry(self.cierreWindow, textvariable=self.propina).place(x=130, y=180)

		tk.Button(self.cierreWindow, text="Cancelar", command=self.cierreWindow.destroy).place(x=50,y=210)
		tk.Button(self.cierreWindow, text="Aceptar", command=self.cerrarCaja).place(x=150,y=210)

	def cerrarCaja(self):
		if self.dinero.get().isdigit():
			self.sistema.cierreDeCaja(self.dinero.get(), self.dineroInicial.get(), self.gastos.get(), self.nomina.get(), self.propina.get(), self.dia.get())

			self.cierreWindow.destroy()
		|

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
		self.numClientes = tk.StringVar()
		self.dinRecibido = tk.StringVar()
		self.propina = tk.StringVar()
		self.total = tk.StringVar()

		tk.Label(self.master, text="Clientes:").place(x=50, y=10)
		tk.Entry(self.master, textvariable=self.numClientes).place(x=110, y=10)

		tk.Label(self.master, text="Propina:").place(x=50, y=30)
		tk.Entry(self.master, textvariable=self.propina).place(x=110, y=30)

		tk.Label(self.master, text="Total:").place(x=65, y=50)
		tk.Entry(self.master, textvariable=self.total).place(x=110, y=50)

		tk.Label(self.master, text="Dinero recibido:").place(x=10, y=70)
		tk.Entry(self.master, textvariable=self.dinRecibido).place(x=110, y=70)

		tk.Button(self.master, text="Aceptar", command=self.callSystem).place(x=185,y=95)
		tk.Button(self.master, text="Borrar", command=self.clearComanda).place(x=125,y=95)

		tk.Label(self.master, text="Consumo:").place(x=40, y=130)
		self.textoConsumo = tk.Text(self.master, width=24, height=5)
		self.textoConsumo.place(x=110, y=130)
		tk.Button(self.master, text="Añadir", command=self.agregar).place(x=260, y=220)
		tk.Button(self.master, text="Calcular", command=self.consumo).place(x=200, y=220)
		tk.Button(self.master, text="Borrar", command=self.clearConsumo).place(x=140,y=220)

	def callSystem(self):
		if self.propina.get() == "":
			self.propina.set("0")
		self.master.withdraw()
		self.sistema.nuevaComanda(self.numClientes.get(), self.total.get(), self.dinRecibido.get(), self.propina.get())
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
			self.numClientes.set("")
			self.dinRecibido.set("")
			self.propina.set("")
			self.total.set("")
		
	def clearConsumo(self):
		self.textoConsumo.delete('1.0', '2.0')

	def consumo(self):
		cons = self.textoConsumo.get("1.0","end").split()
		try:
			cons = [int(x) for x in cons]
			cons = self.sistema.calculoComanda(cons)
			self.total.set(cons["Total"])
			self.propina.set(cons["Propina"])
		except ValueError:
			self.consWindow = tk.Toplevel(self)
			self.consWindow.wm_title("Resultado")
			self.consWindow.geometry("200x150")
			tk.Label(self.consWindow, text="Error!").place(x=30, y=20)
			tk.Button(self.consWindow, text="Aceptar", command=self.consWindow.destroy).place(x=75,y=90)
		
	def agregar(self):
		cons = self.textoConsumo.get("1.0","end").split()
		try:
			cons = [int(x) for x in cons]
			if self.total.get() == "":
				cons = self.sistema.calculoComanda(cons)
			else:
				cons = self.sistema.calculoComanda(cons + [int(self.total.get())])
			self.total.set(cons["Total"])
			self.propina.set(cons["Propina"])
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