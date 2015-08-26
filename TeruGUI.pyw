import tkinter as tk
import SistemaTeru
		
class MesaGUI(tk.Frame):
	"""Aquí es donde se se hace la comanda para una mesa"""
	def __init__(self, sistema=SistemaTeru.MainSystem(), nombreMesa="", master=None):
		tk.Frame.__init__(self, master)
		self.nombreMesa = nombreMesa
		self.master.title("Comanda: " + str(self.nombreMesa.get()))
		self.master.geometry("480x270")
		self.pack()
		self.sistema = sistema
		self.createWidgets()

	def createWidgets(self):
		self.numClientes = tk.StringVar()
		self.dinRecibido = tk.StringVar()
		self.propina = tk.StringVar()
		self.total = tk.StringVar()
		self.tarjeta = tk.IntVar()

		tk.Label(self.master, text="Clientes:").place(x=50, y=10)
		tk.Entry(self.master, textvariable=self.numClientes).place(x=110, y=10)

		tk.Label(self.master, text="Cambiar Nombre:").place(x=300, y=10)
		tk.Entry(self.master, textvariable=self.nombreMesa, width=10).place(x=410, y=10)
		tk.Button(self.master, text="Cambiar", command=self.cambiarMesa).place(x=415, y=35)

		tk.Label(self.master, text="Propina:").place(x=50, y=30)
		tk.Entry(self.master, textvariable=self.propina).place(x=110, y=30)

		tk.Label(self.master, text="Total:").place(x=65, y=50)
		tk.Entry(self.master, textvariable=self.total).place(x=110, y=50)

		tk.Label(self.master, text="Dinero recibido:").place(x=10, y=70)
		tk.Entry(self.master, textvariable=self.dinRecibido).place(x=110, y=70)
		tk.Checkbutton(self.master, text="Tarjeta:", variable=self.tarjeta).place(x=250, y=70)

		tk.Button(self.master, text="Aceptar", command=self.confirmarComanda).place(x=185,y=95)
		tk.Button(self.master, text="Borrar", command=self.clearComanda).place(x=125,y=95)

		tk.Label(self.master, text="Consumo:").place(x=40, y=130)
		self.textoConsumo = tk.Text(self.master, width=24, height=5)
		self.textoConsumo.place(x=110, y=130)
		tk.Button(self.master, text="Añadir", command=self.agregar).place(x=260, y=220)
		tk.Button(self.master, text="Calcular", command=self.consumo).place(x=200, y=220)
		tk.Button(self.master, text="Borrar", command=self.clearConsumo).place(x=140,y=220)

	def cambiarMesa(self):
		if self.nombreMesa.get() != "":
			self.master.title("Comanda: " + str(self.nombreMesa.get()))

	def confirmarComanda(self):
		if self.propina.get() == "":
			self.propina.set("0")
		self.master.withdraw()
		self.sistema.nuevaComanda(self.numClientes.get(), self.total.get(), self.dinRecibido.get(), self.propina.get(), bool(self.tarjeta.get()))
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

class CierreGUI(tk.Frame):
	"""docstring for cierreGUI"""
	def __init__(self, sistema=SistemaTeru.MainSystem(), master=None, padre=None):
		tk.Frame.__init__(self, master)		
		self.padre = padre
		self.sistema = sistema
		self.padre.withdraw()
		self.master.wm_title("Cierre")
		self.master.geometry("280x250")
		self.pack()
		self.createWidgets()

	def createWidgets(self):
		self.dinero = tk.StringVar()
		self.gastos = tk.StringVar()
		self.nomina = tk.StringVar()
		self.dineroInicial = tk.StringVar()
		self.dia = tk.StringVar()
		self.dineroLlevo = tk.StringVar()

		tk.Label(self.master, text="Fecha (dd-mm-año):").place(x=10,y=10)
		tk.Entry(self.master, textvariable=self.dia).place(x=130, y=10)
		tk.Label(self.master, text="Nota: Dejar vacío si se quiere el día de hoy").place(x=30,y=30)
		tk.Label(self.master, text="Dinero en caja:").place(x=45,y=60)
		tk.Entry(self.master, textvariable=self.dinero).place(x=130, y=60)
		tk.Label(self.master, text="Dinero Inicial:").place(x=50,y=90)
		tk.Entry(self.master, textvariable=self.dineroInicial).place(x=130, y=90)
		tk.Label(self.master, text="Gastos:").place(x=85,y=120)
		tk.Entry(self.master, textvariable=self.gastos).place(x=130, y=120)
		tk.Label(self.master, text="Nómina(Total):").place(x=45,y=150)
		tk.Entry(self.master, textvariable=self.nomina).place(x=130, y=150)

		tk.Button(self.master, text="Cancelar", command=self.showMain).place(x=50,y=180)
		tk.Button(self.master, text="Aceptar", command=self.cerrarCaja).place(x=150,y=180)

	def cerrarCaja(self):
		"""
		Llama al sistema para cerrar caja con los datos introducidos en la ventana CerrarCaja
		"""
		if self.dinero.get().isdigit():

			self.master.withdraw()
			self.reporteWindow = tk.Toplevel(self)
			self.reporteWindow.wm_title("Reporte del día")
			self.reporteWindow.geometry("280x280")

			reporte = self.sistema.cierreDeCaja(self.dinero.get(), self.dineroInicial.get(), self.gastos.get(), self.nomina.get(), self.dia.get())
			cadReporte = reporte[0].split(",")
			cadReporte = "Total Mesas: " + cadReporte[1] + "\nTotal Clientes: " + cadReporte[2] + \
			"\nCaja: " + cadReporte[3] + "\nCobro Efectivo: " + cadReporte[4] + "\nTerminal: " + cadReporte[5] + \
			"\nGastos: " + cadReporte[6] + "\nSueldo: " + cadReporte[7] + "\nNeto: " + cadReporte[8] + "\nDinero: " + cadReporte[9] + \
			"\nSobra/Falta: " + cadReporte[10] + "\nPropinas: " + str(reporte[1])
			
			tk.Label(self.reporteWindow, text=cadReporte).place(x=80, y=10)
			tk.Label(self.reporteWindow, text="Llevo: ").place(x=60, y=180)
			tk.Entry(self.reporteWindow, textvariable=self.dineroLlevo).place(x=100, y=180)
			tk.Button(self.reporteWindow, text="Cancelar", command=self.reporteWindow.destroy).place(x=50,y=210)
			tk.Button(self.reporteWindow, text="Aceptar", command=self.aceptarCierre).place(x=150,y=210)

	def aceptarCierre(self):
		self.sistema.commitCierre(self.dineroLlevo.get(), self.dia.get())
		print(self.dia.get())
		self.reporteWindow.destroy()
		self.showMain()

	def showMain(self):
		self.padre.abrirVentana()
		self.master.destroy()

	def cancelarReporte(self):
		self.reporteWindow.destroy()
		self.master.update()
		self.master.deiconify()

class Instanciador(tk.Frame):
	"""
		Ventana principal donde se sacaran nuevas comandas y se hará el cierre de caja
	"""
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.master.title("Teru Sistema")
		self.master.geometry("170x180")
		self.pack()
		self.createWidgets()

	def createWidgets(self):
		self.contador = 0
		self.sistema = SistemaTeru.MainSystem()
		self.textContador = tk.StringVar()
		self.nombreMesa = tk.StringVar()
		self.textContador.set("Mesas: " + str(self.contador))
		self.folioLabel = tk.Label(self.master, textvariable=self.textContador).place(x=60, y=10)
		tk.Label(self.master, text="Nombre Mesa:").place(x=10,y=40)
		tk.Entry(self.master, text="Nombre Mesa:", width=10, textvariable=self.nombreMesa).place(x=100,y=40)
		tk.Button(self.master, text="Nueva Mesa", command=self.nuevaMesa).place(x=50,y=70)
		tk.Button(self.master, text="Cierre de caja", command=self.datosCierre).place(x=45,y=110)

	def nuevaMesa(self):
		"""
			Se abre una nueva ventana para cobrar una mesa
		"""
		self.contador += 1
		self.textContador.set("Mesas: " + str(self.contador))
		MesaGUI(self.sistema, self.nombreMesa, tk.Toplevel(self))

	def datosCierre(self):
		"""
		Accion para el boton "Cierre de Caja", nos pide los datos de cierre de caja y hacer la acción
		"""
		CierreGUI(self.sistema, tk.Toplevel(self), self)		

	def withdraw(self):
		self.master.withdraw()

	def abrirVentana(self):
		self.master.update()
		self.master.deiconify()

if __name__ == '__main__':
	root = tk.Tk()
	app = Instanciador(master=root)
	app.mainloop()