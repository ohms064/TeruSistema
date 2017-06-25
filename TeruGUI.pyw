import tkinter as tk
from Sistema.parserUtils import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from Sistema.tkUtils import *
from Sistema.SistemaTeru import *
from Sistema.tkUtils import *
from Sistema.CustomTK import UserForm
import json
import sys
import copy
import Datos.Platillos
		
class MesaGUI(tk.Frame):
	"""
	Aquí es donde se se hace la comanda para una mesa
	Esta clase es llamada desde Instanciador y puede instanciar tantas MesaGUI como sea necesario.
	"""
	def __init__(self, sistema, nombreMesa="", master=None, padre=None):
		tk.Frame.__init__(self, master)
		self.nombreMesa = nombreMesa
		self.padre = padre
		self.master.title("Comanda: " + str(self.nombreMesa.get()))
		self.master.geometry("540x350")
		self.pack()
		self.sistema = sistema
		self.master.protocol("WM_DELETE_WINDOW", self.onCloseWindow)
		self.pedido = self.sistema.nuevoPedido()
		self.selectedItem = -1
		self.createWidgets()
		self.createMenu()

	def createMenu(self):
		self.mainMenu = tk.Menu(self.master)
		self.categorias = self.sistema.platillosDB.getCategories()
		self.subMenus = dict()
		for categoria in self.categorias:
			if categoria == "Extra":
				continue
			self.subMenus[categoria] = tk.Menu(self.master, tearoff=0)
			platCategoria = self.sistema.platillosDB.buscarCategoria(categoria)
			for platillo in platCategoria:
				self.subMenus[categoria].add_command(label=platillo.nombre, command=self.agregarAPedido(platillo, self.pedido))
			self.mainMenu.add_cascade(label=categoria, menu=self.subMenus[categoria])

		self.master.config(menu=self.mainMenu)

	def agregarAPedido(self, platillo, pedido):
		def agregar():
			#Este será el comportamiento por default
			index = pedido.agregar(platillo)
			if index != -1:
				self.actualizarListbox(index, pedido.orden[index][1], command="cantidad")
			else:
				self.agregarAlListbox(pedido.obtenerString(-1))#Obtener el string del platillo que acabamos de agregar
		def completarPlatillo():
			plugin = self.sistema.loadPlugin(platillo)

			if plugin is None:
				#Para cualquier error se procederá normalmente
				print("Plugin no encontrado")
				self.sistema.escribirError("No se encontró el plugin: {} del platillo {}", platillo.pluginName, str(platillo))
				agregar()
				return

			results = plugin.createWindowWait(tk.Toplevel(self), self.master)
			if "$Cancel$" in results:
				return
			index = plugin.updatePedido(pedido, results, platillo)

			if index != -1:
				self.actualizarListbox(index, pedido.orden[index], command="todo")
			else:
				self.agregarAlListbox(pedido.obtenerString(-1))

		if platillo.pluginName:
			return completarPlatillo
		return agregar

	def createWidgets(self):
		"""
		Este método es llamado siempre desde init, se crean todos los widgets dentro de la ventana
		"""
		self.numClientes = tk.StringVar()
		self.dinRecibido = tk.StringVar()
		self.propina = tk.StringVar()
		self.total = tk.StringVar()
		self.tarjeta = tk.IntVar()
		self.idCliente = tk.StringVar()

		vcmd = (self.master.register(validate ),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

		tk.Label(self.master, text="Clientes:").place(x=50, y=10)
		tk.Entry(self.master, textvariable=self.numClientes).place(x=110, y=10)

		tk.Label(self.master, text="Propina:").place(x=50, y=30)
		tk.Entry(self.master, textvariable=self.propina).place(x=110, y=30)

		tk.Label(self.master, text="Consumo:").place(x=40, y=50)
		tk.Label(self.master, textvariable=self.total).place(x=110, y=50)

		tk.Label(self.master, text="Dinero recibido:").place(x=10, y=70)
		tk.Entry(self.master, textvariable=self.dinRecibido).place(x=110, y=70)
		tk.Checkbutton(self.master, text="Tarjeta:", variable=self.tarjeta).place(x=250, y=70)

		tk.Label(self.master, text="ID Cliente:").place(x=40, y=90)
		tk.Entry(self.master, textvariable=self.idCliente).place(x=110, y=90)

		tk.Button(self.master, text="Aceptar", command=self.confirmarComanda).place(x=185,y=115)
		#tk.Button(self.master, text="Borrar", command=self.clearComanda).place(x=125,y=115)

		tk.Label(self.master, text="Cambiar Nombre:").place(x=320, y=100)
		tk.Entry(self.master, textvariable=self.nombreMesa, width=10).place(x=430, y=100)
		tk.Button(self.master, text="Cambiar", command=self.cambiarMesa).place(x=435, y=125)

		tk.Label(self.master, text="Mesa:").place(x=350,y=20)
		self.labelMesa = tk.Label(self.master, text=self.nombreMesa.get()[:2], font=("Times", 50))
		self.labelMesa.place(x=420,y=0)

		tk.Label(self.master, text="Id").place(x=13, y=155)
		tk.Label(self.master, text="Nombre").place(x=35, y=155)
		tk.Label(self.master, text="Precio").place(x=260, y=155)
		tk.Label(self.master, text="Categoría").place(x=320, y=155)
		tk.Label(self.master, text="Cantidad").place(x=385, y=155)

		self.total.set(0)

		#Platillos
		frame, self.pedidoListbox = createListbox(self.master, width=60)
		self.pedidoListbox.bind("<Double-Button-1>", self.listBoxSelect)
		frame.place(x=10, y=175)

		tk.Button(self.master, text="Borrar", command=self.borrarArticulo).place(x=460, y=275)
		tk.Button(self.master, text="Borrar Todo", command=self.borrarTodo).place(x=460, y=305)

	def listBoxSelect(self, event):
		widget = event.widget
		self.selectedItem = widget.curselection()[0]

	def agregarAlListbox(self, platillo):
		self.pedidoListbox.insert(tk.END, str(platillo))
		total = self.pedido.obtenerTotal()
		self.total.set(total)
		#self.propina.set(int(total*0.1))

	def borrarArticulo(self):
		if self.selectedItem == -1:
			return
		self.pedidoListbox.delete(self.selectedItem)
		del self.pedido.orden[self.selectedItem]
		self.selectedItem = -1
		total = self.pedido.obtenerTotal()
		self.total.set(total)

	def borrarTodo(self):
		clearListbox(self.pedidoListbox)
		self.pedido.clear()
		self.selectedItem = -1
		total = self.pedido.obtenerTotal()
		self.total.set(total)

	def actualizarListbox(self, index, value, command="cantidad"):
		current = self.pedido.get(index, platillo=False)
		if command == "cantidad":
			current[1] = value
		elif command == "precio":
			current[0].precio = value
		elif command == "incrementar":
			current[1] += value
		elif command == "todo":
			curent = value
		updateListbox(self.pedidoListbox, index, self.pedido.obtenerString(current))
		self.total.set(self.pedido.obtenerTotal())

	def cambiarMesa(self):
		"""
		Se el asigna el nombre a la mesa en caso de que no exista o se quiera cambiar.
		El nombre aparece en el título de la ventana.
		"""
		if self.nombreMesa.get() != "":
			self.master.title("Comanda: " + str(self.nombreMesa.get()))
			self.labelMesa.config(text=self.nombreMesa.get()[:2])
			self.nombreMesa.set("")

	def confirmarComanda(self):
		"""
		Se confirma que la comanda sea correcta.
		Se existe algún error se abrirá una ventana indicando que hay un error.(Cualquier error)
		"""
		self.master.withdraw()
		checkVar(self.numClientes, "0")
		checkVar(self.dinRecibido, "0")
		checkVar(self.propina, "0")
		if checkVar(self.total, "0"):
			mb.showinfo("Total", "No se ha escrito el consumo")
			self.show()
			return

		comanda = self.sistema.nuevaComanda(self.numClientes.get(), self.total.get(), self.dinRecibido.get(), self.propina.get(), bool(self.tarjeta.get()), self.idCliente.get(), self.pedido)
		if self.sistema:
			mb.showinfo("¡Error!", "Se ha producido un error. TeruGUI 200 confirmarComanda.\nRevisar que los datos sean correctos.")
			self.show()
		else:
			if mb.askokcancel("Comanda", comanda.cobro()):
				self.aceptarComanda(comanda)
			else:
				self.show()

	def clearComanda(self):
		"""
		Se limpian los datos de la comanda.
		"""
		self.numClientes.set("")
		self.dinRecibido.set("")
		self.propina.set("")
		self.total.set("")

	def aceptarComanda(self, comanda):
		"""
		Se confirma la comanda.
		"""
		self.sistema.commitComanda(comanda)
		self.clearComanda()

	def show(self):
		"""
		Se regresa a MesaGUI
		"""
		self.master.update()
		self.master.deiconify()

	def onCloseWindow(self):
		self.padre.reducirMesa()
		self.master.destroy()

class CierreGUI(tk.Frame):
	"""
	En esta ventana se maneja todo lo conciernente al cierre de caja.
	"""
	def __init__(self, sistema, master=None, padre=None):
		tk.Frame.__init__(self, master)		
		self.padre = padre
		self.sistema = sistema
		self.padre.withdraw()
		self.master.wm_title("Cierre")
		self.master.geometry("280x250")
		self.pack()
		self.createWidgets()
		self.master.protocol("WM_DELETE_WINDOW", self.showMain)

	def createWidgets(self):
		"""
		Se crean todos los widgets de la ventana.
		"""
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
			"\nDinero Inicial: " + cadReporte[3] + "\Ventas Efectivo: " + cadReporte[4] + "\nTerminal: " + cadReporte[5] + \
			"\nGastos: " + cadReporte[6] + "\nNomina: " + cadReporte[7] + "\nNeto: " + cadReporte[8] + "\nDinero: " + cadReporte[9] + \
			"\nSobra/Falta: " + cadReporte[10] + "\nPropinas: " + str(reporte[1])
			
			tk.Label(self.reporteWindow, text=cadReporte).place(x=80, y=10)
			tk.Label(self.reporteWindow, text="Llevo: ").place(x=60, y=180)
			tk.Entry(self.reporteWindow, textvariable=self.dineroLlevo).place(x=100, y=180)
			tk.Button(self.reporteWindow, text="Cancelar", command=self.cancelarReporte).place(x=50,y=210)
			tk.Button(self.reporteWindow, text="Aceptar", command=self.aceptarCierre).place(x=150,y=210)

	def aceptarCierre(self):
		"""
		Se confirma el cierre.
		"""
		self.sistema.commitCierre(self.dineroLlevo.get(), self.dia.get())
		self.reporteWindow.destroy()
		self.showMain()

	def showMain(self):
		"""
		Se retorna a la ventana padre.
		"""
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
		self.master.geometry("170x260")
		self.pack()
		master.protocol("WM_DELETE_WINDOW", self.onCloseWindow)
		self.sistema = MainSystem()
		self.createWidgets()

	def createWidgets(self):
		self.textContador = tk.StringVar()
		self.nombreMesa = tk.StringVar()
		self.textContador.set("Mesas: " + str(self.sistema.conf["visitas"]))
		self.folioLabel = tk.Label(self.master, textvariable=self.textContador).place(x=60, y=10)
		tk.Label(self.master, text="Nombre Mesa:").place(x=10,y=40)
		tk.Entry(self.master, width=10, textvariable=self.nombreMesa).place(x=100,y=40)
		tk.Button(self.master, text="Nueva Mesa", command=self.nuevaMesa).place(x=50,y=70)
		tk.Button(self.master, text="Cierre de caja", command=self.datosCierre).place(x=45,y=110)
		tk.Button(self.master, text="Estado Actual", command=self.estadoActual).place(x=45, y=150)
		tk.Button(self.master, text="Clientes", command=self.abrirClientesGUI).place(x=55, y=190)
		tk.Button(self.master, text="Platillos", command=self.abrirPlatillosGUI).place(x=55, y=230)

	def estadoActual(self):
		estado = self.sistema.getState()
		self.estadoWindow = tk.Toplevel(self)
		self.estadoWindow.wm_title("Estado Actual")
		self.estadoWindow.geometry("250x180")
		tk.Label(self.estadoWindow, text=estado).place(x=80, y=10)

	def abrirPlatillosGUI(self):
		PlatillosGUI(self.sistema, tk.Toplevel(self), self)

	def abrirClientesGUI(self):
		"""
		Acción para el botón "Clientes" cuya ventana es para hacer acciones sobre la tabla de clientes
		"""
		ClientesGUI(self.sistema, tk.Toplevel(self), self)

	def nuevaMesa(self):
		"""
			Se abre una nueva ventana para cobrar una mesa
		"""
		self.sistema.conf["visitas"] += 1
		self.textContador.set("Mesas: " + str(self.sistema.conf["visitas"]))
		MesaGUI(self.sistema, self.nombreMesa, tk.Toplevel(self), self)

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

	def reducirMesa(self):
		self.sistema.conf["visitas"] -= 1
		self.textContador.set("Mesas: " + str(self.sistema.conf["visitas"]))

	def onCloseWindow(self):
		try:
			print("Cerrando sistema")
			del self.sistema
		except:
			pass
		print("Terminando ciclo")
		self.master.eval('::ttk::CancelRepeat')
		print("Destruyendo ventana")
		self.master.destroy()
		print("Se cerró el programa")
		
class ClientesGUI(tk.Frame):
	"""
	En esta ventana se verán todas las acciones relacionados con la base de datos de los clientes.
	"""
	def __init__(self, sistema, master=None, padre=None):
		tk.Frame.__init__(self, master)		
		self.padre = padre
		self.sistema = sistema
		self.master.wm_title("Clientes")
		self.master.geometry("400x130")
		self.pack()
		self.createWidgets()
		self.master.protocol("WM_DELETE_WINDOW", self.showMain)

	def createWidgets(self):
		self.id = tk.StringVar()
		self.nick = tk.StringVar()
		self.correo = tk.StringVar()
		self.nombre = tk.StringVar()
		self.visitas = tk.StringVar()
		self.ultimaVisita = tk.StringVar()
		self.consumo = tk.StringVar()
		self.fechaIngreso = tk.StringVar()

		#Sección de la izquierda
		tk.Label(self.master, text="ID: ").place(x=30, y=10)
		tk.Entry(self.master, width=30, textvariable=self.id).place(x=60, y=10)
		tk.Label(self.master, text="Nick: ").place(x=20, y=30)
		tk.Entry(self.master, width=30, textvariable=self.nick).place(x=60, y=30)
		tk.Label(self.master, text="Correo: ").place(x=10, y=50)
		tk.Entry(self.master, width=30, textvariable=self.correo).place(x=60, y=50)
		tk.Label(self.master, text="Nombre: ").place(x=3, y=70)
		tk.Entry(self.master, width=30, textvariable=self.nombre).place(x=60, y=70)

		#Sección de la derecha
		tk.Label(self.master, text="Visitas: ").place(x=280, y=10)
		tk.Label(self.master, textvariable=self.visitas, bd=1).place(x=330, y=10)
		tk.Label(self.master, text="Ultima Visita: ").place(x=250, y=30)
		tk.Label(self.master, textvariable=self.ultimaVisita).place(x=330, y=30)
		tk.Label(self.master, text="Consumo:").place(x=265, y=50)
		tk.Label(self.master, textvariable=self.consumo).place(x=330, y=50)
		tk.Label(self.master, text="Ingreso:").place(x=275, y=70)
		tk.Label(self.master, textvariable=self.fechaIngreso).place(x=330, y=70)

		#Sección de abajo
		tk.Button(self.master, text="Buscar", command=self.busqueda).place(x=10, y=100)
		tk.Button(self.master, text="Insertar", command=self.insertar).place(x=65, y=100)
		tk.Button(self.master, text="Borrar", command=self.borrar).place(x=125, y=100)
		tk.Button(self.master, text="Actualizar", command=self.actualizar).place(x=180, y=100)
		tk.Button(self.master, text="Limpiar Campos", command=self.cls).place(x=270, y=100)
		

	def busqueda(self, identificador=""):
		"""
		Función para el botón de Buscar que funciona de la siguiente manera:
		En esta función si se envía como argumento el identificador se utilizará este ID
		para hacer la busqueda. De no ser así se hará el busqueda con la siguiente jerarquía:
			id -> nick -> correo -> nombre
		Es decir que si no se tiene escrito el id en su campo se buscará por nick y así sucesivamente.
		"""
		try:
			if identificador:
				query = self.sistema.clientesDB.buscarID(identificador)
			elif self.id.get():
				query = self.sistema.clientesDB.buscarID(self.id.get())
			elif self.nick.get():
				query = self.sistema.clientesDB.buscarNick(self.nick.get())
			elif self.correo.get():
				query = self.sistema.clientesDB.buscarCorreo(self.correo.get())
			elif self.nombre.get():
				query = self.sistema.clientesDB.buscarNombre(self.nombre.get())
			else:
				mb.showinfo("Error", "No se ingresaron datos", parent=self.master)
				return
		except:
			mb.showinfo(sys.exc_info()[0])
			return
		self.id.set(query.id)
		self.nick.set(query.nick)
		self.correo.set(query.correo)
		self.nombre.set(query.nombre)
		self.visitas.set(query.visitas)
		self.ultimaVisita.set(query.ultimaVisita)
		self.consumo.set(query.consumo)
		self.fechaIngreso.set(query.fechaIngreso)

	def insertar(self):
		"""
		Función para el botón de insertar que funciona de la siguiente manera:
		Se ingresará nick, correo y/o nombre, con esto se creará un nuevo cliente con un nuevo ID.
		"""
		if self.nombre.get() == "" and self.nick.get() == "" and self.correo.get() == "":
			mb.showinfo("Warning", "¡No se agregó ningún dato!", parent=self.master)
			return

		answer = mb.askquestion("Insertar", "¿Son correctos los datos?", icon="warning", parent=self.master)
		if answer == "yes":
			try:
				self.sistema.clientesDB.insertar(nombre=self.nombre.get(), correo=self.correo.get(), nick=self.nick.get())
				self.sistema.clientesDB.confirmar()
			except:
				mb.showinfo("Error", "Error al insertar. Ya existe el correo.")
				return
			self.busqueda(len(self.sistema.clientesDB))

	def borrar(self):
		"""
		Función para el botón de borrar que funciona de la siguiente manera:
		Se ingresará únicamente el ID, lo demás será ignorado. Se borrará el cliente con este ID.
		"""
		if self.id.get() == "":
			mb.showinfo("Advertencia", "¡Se debe ingresar un ID!", parent=self.master)
			return
		self.busqueda(self.id.get())
		if self.id.get() == "¡ERROR! No se encontró información":
			mb.showinfo("¡Error!", "No se encontraron coincidencias. No se continuará con el proceso.", parent=self.master)
			self.cls()
			return
		answer = mb.askquestion("Borrar", "Los datos se perderán permanentemente. Favor de revisar.", parent=self.master)
		if answer == "yes":
			try:
				self.sistema.clientesDB.borrar(self.id.get())
				self.sistema.clientesDB.confirmar()
			except:
				mb.showinfo(sys.exc_info()[0])
				return
			self.cls()

	def actualizar(self):
		"""
		Función para el botón que actualiza los datos de la siguiente manera:
		Se ingresa el ID (el cliente con este ID será modificado) y se ingresa solamente los datos que se quieran
		cambiar. Una vez hecho esto al dar click en Actualizar se nos mostrará los cambios que se harán y nos
		preguntará si es correcto.
		"""
		#Primero vemos que exista el ID
		if self.id.get() == "":
			mb.showinfo("Advertencia", "¡Se debe ingresar un ID!", parent=self.master)
			return
		#No tiene caso hacer nada si ningún valor se ha introducido
		if self.nick.get() == "" and self.nombre.get() == "" and self.correo.get() == "":
			mb.showinfo("Advertencia", "¡No se ingresó ningún cambio!", parent=self.master)
			return
		#Variables auxiliares que son los nuevos valores potenciales
		nick = self.nick.get().strip()
		nombre = self.nombre.get().strip()
		correo = self.correo.get().strip()
		#Se hace una busqueda para poder mostrar los valores originales
		self.busqueda(self.id.get())
		#Si no se encontró el ID se nos indicará
		if self.id.get() == "¡ERROR! No se encontró información":
			mb.showinfo("¡Error!", "No se encontraron coincidencias. No se continuará con el proceso.", parent=self.master)
			self.cls()
			return
		#Para cada valor potencial, si tiene escrito algo se escribirá en el campo de la siguiente manera: {ORIGNAL} -> {NUEVO}
		if nick:
			self.nick.set(self.nick.get() + " -> " + nick)
		if nombre:
			self.nombre.set(self.nombre.get() + " -> " + nombre)
		if correo:
			self.correo.set(self.correo.get() + " -> " + correo)
		#Se nos preguntará si continuamos con el proceso
		answer = mb.askquestion("Actualizar", "¿Son correctos los datos a actualizar?")
		if answer == "yes":
			try:#Puede que la base de datos estuviera bloqueada
				self.sistema.clientesDB.actualizar(self.id.get(), nombre=nombre, nick=nick, correo=correo)
				self.sistema.clientesDB.confirmar()
			except:
				mb.showinfo(sys.exc_info()[0])
				return
			self.busqueda(self.id.get())
		else:
			self.nick.set(nick)
			self.nombre.set(nombre)
			self.correo.set(correo)

	def cls(self):
		self.id.set("")
		self.nick.set("")
		self.correo.set("")
		self.nombre.set("")
		self.visitas.set("")
		self.ultimaVisita.set("")
		self.consumo.set("")
		self.fechaIngreso.set("")

	def showMain(self):
		"""
		Se retorna a la ventana padre.
		"""
		self.master.destroy()

class PlatillosGUI(tk.Frame):
	def __init__(self, sistema, master=None, padre=None):
		tk.Frame.__init__(self, master)		
		self.padre = padre
		self.sistema = sistema
		self.master.wm_title("Platillos")
		self.master.geometry("1100x360")
		self.pack()
		self.createWidgets()
		self.createMenu()
		self.populatePlatillos()
		self.populateIngredientes()
		self.master.protocol("WM_DELETE_WINDOW", self.showMain)

	def createMenu(self):
		self.mainMenu = tk.Menu(self.master)
		self.categorias = self.sistema.platillosDB.getCategories()
		self.importMenu = tk.Menu(self.master, tearoff=0)
		self.importMenu.add_command(label="Importar Platillos desde CSV", command=self.platillosfromCSV)
		self.importMenu.add_command(label="Importar Ingredientes desde CSV", command=self.ingredientesfromCSV)
		self.mainMenu.add_cascade(label="Importar", menu=self.importMenu)
		self.master.config(menu=self.mainMenu)

	def createWidgets(self):
		self.idPlatillo = tk.StringVar()
		self.nombre = tk.StringVar()
		self.precio = tk.StringVar()
		self.categoria = tk.StringVar()
		self.nuevaCategoria = tk.StringVar()
		self.plugin = tk.StringVar()

		tk.Label(self.master, text="Platillos").place(x=30, y=10)

		platillosFrame, self.platillosListbox = createListbox(self.master, width=60)
		platillosFrame.place(x=30, y=30)
		self.platillosListbox.bind("<Double-Button-1>", self.platillosListBoxSelect)
	
		tk.Label(self.master, text="Datos Platillo").place(x=30, y=210)

		tk.Label(self.master, text="Id").place(x=30, y=230)
		tk.Entry(self.master, width=30, textvariable=self.idPlatillo).place(x=90, y=230)

		tk.Label(self.master, text="Nombre").place(x=30, y=250)
		tk.Entry(self.master, width=30, textvariable=self.nombre).place(x=90, y=250)

		tk.Label(self.master, text="Precio").place(x=30, y=270)
		tk.Entry(self.master, width=30, textvariable=self.precio).place(x=90, y=270)

		tk.Label(self.master, text="Categoría").place(x=30, y=290)
		self.cb = ttk.Combobox(self.master, width=27, textvariable=self.categoria, value=self.sistema.conf["Categorias Platillo"], state="readonly")
		self.cb.place(x=90, y=290)

		tk.Label(self.master, text="Nueva Categoría").place(x=290, y=290)
		tk.Entry(self.master, width=20, textvariable=self.nuevaCategoria).place(x=400, y=290)
		tk.Button(self.master, text="Agregar", command=self.actualizarCategorias).place(x=470, y=320)

		tk.Label(self.master, text="Config").place(x=315, y=230)
		tk.Entry(self.master, width=25, textvariable=self.plugin).place(x=370, y=230)

		tk.Button(self.master, text="Insertar", command=self.insertarPlatillo).place(x=220, y=320)
		tk.Button(self.master, text="Actualizar", command=self.actualizarPlatillo).place(x=152, y=320)
		tk.Button(self.master, text="Borrar", command=self.borrarPlatillo).place(x=105, y=320)

		#Ingrediente Platillo
		self.idIngredientePlatillo = tk.StringVar()
		self.porcionIngredientePlatillo = tk.StringVar()
		self.unidadIngredientePlatillo = tk.StringVar()
		tk.Label(self.master, text="Ingrediente Platillo").place(x=540, y=10)

		ingredientesPlatilloFrame, self.ingredientesPlatilloListbox = createListbox(self.master, width=30)
		ingredientesPlatilloFrame.place(x=540, y=30)

		tk.Label(self.master, text="Datos Ingrediente para Platillo").place(x=540, y=210)
		
		tk.Label(self.master, text="Id").place(x=540, y=230)
		tk.Entry(self.master, width=10, textvariable=self.idIngredientePlatillo).place(x=595, y=230)
		tk.Label(self.master, text="Porción").place(x=540, y=250)
		tk.Entry(self.master, width=15, textvariable=self.porcionIngredientePlatillo).place(x=595, y=250)
		ttk.Combobox(self.master, width=10, textvariable=self.unidadIngredientePlatillo, values=self.sistema.unidadDB.nombres).place(x=695, y=250)
		
		tk.Button(self.master, text="Agregar Ingrediente", command=self.insertarIngredientePlatillo).place(x=540, y=320)
		tk.Button(self.master, text="Borrar Ingrediente", command=self.borrarIngredientePlatillo).place(x=670, y=320)

		#Ingredientes
		self.idIngrediente = tk.StringVar()
		self.nombreIngrediente = tk.StringVar()
		self.cantidadIngrediente = tk.StringVar()
		self.unidadIngrediente = tk.StringVar()
		tk.Label(self.master, text="Ingrediente").place(x=820, y=10)		

		ingredienteFrame, self.ingredienteListbox = createListbox(self.master, width=30)
		ingredienteFrame.place(x=820, y=30)
		self.ingredienteListbox.bind("<Double-Button-1>", self.ingredienteListBoxSelect)

		tk.Label(self.master, text="Datos Ingrediente").place(x=820, y=210)
		tk.Label(self.master, text="Id").place(x=820, y=230)
		tk.Entry(self.master, width=30, textvariable=self.idIngrediente).place(x=875, y=230)
		tk.Label(self.master, text="Nombre").place(x=820, y=250)
		tk.Entry(self.master, width=30, textvariable=self.nombreIngrediente).place(x=875, y=250)
		tk.Label(self.master, text="Cantidad").place(x=820, y=270)
		tk.Entry(self.master, width=15, textvariable=self.cantidadIngrediente).place(x=875, y=270)
		ttk.Combobox(self.master, width=10, textvariable=self.unidadIngrediente, values=self.sistema.unidadDB.nombres).place(x=975, y=270)

		tk.Button(self.master, text="Insertar", command=self.insertarIngrediente).place(x=940, y=320)
		tk.Button(self.master, text="Actualizar", command=self.actualzarIngrediente).place(x=870, y=320)
		tk.Button(self.master, text="Borrar", command=self.borrarIngrediente).place(x=820, y=320)

	def insertarIngredientePlatillo(self):
		try:
			idIngrediente = int(self.idIngrediente.get())
			idPlatillo = int(self.idPlatillo.get())
			porcion = float(self.porcionIngredientePlatillo.get())
		except Exception as err:
			print(err)
			return
		unidad = self.unidadIngredientePlatillo.get()
		if not unidad:
			return

		ingrediente = IngredientePlatillo(idIngrediente=idIngrediente, idPlatillo=idPlatillo, porcion=porcion, unidadPorcion=unidad)
		self.sistema.ingredientesDB.insertarIngredientePlatillo(ingrediente)
		self.sistema.ingredientesDB.confirmar()
		clearListbox(self.ingredientesPlatilloListbox)
		self.populateIngredientesPlatillo(idPlatillo)

	def borrarIngredientePlatillo(self):
		pass

	def insertarIngrediente(self):
		nombre = self.nombreIngrediente.get()
		try:
			cantidad = float(self.cantidadIngrediente.get())
		except Exception as err:
			print(err)
			return
		unidad = self.unidadIngrediente.get()
		if nombre and unidad:
			ingrediente = Ingrediente(nombre=nombre, cantidad=cantidad, unidadCantidad=unidad)
			self.sistema.ingredientesDB.insertarIngrediente(ingrediente)
			clearListbox(self.ingredienteListbox)
			self.populateIngredientes()
			self.sistema.ingredientesDB.confirmar()

	def borrarIngrediente(self):
		pass

	def actualzarIngrediente(self):
		pass

	def actualizarCategorias(self):
		self.sistema.conf["Categorias Platillo"].append(self.nuevaCategoria.get())
		self.cb.configure(value=self.sistema.conf["Categorias Platillo"])
		#self.cb["values"] = self.sistema.conf["Categorias Platillo"]

	def platillosListBoxSelect(self, event):
		widget = event.widget
		selection = widget.curselection()[0]
		value = self.platillos[selection]
		self.idPlatillo.set(value.idPlatillo)
		self.precio.set(value.precio)
		self.categoria.set(value.categoria)
		self.nombre.set(value.nombre)
		self.plugin.set(value.pluginName)
		clearListbox(self.ingredientesPlatilloListbox)
		self.populateIngredientesPlatillo(value.idPlatillo)

	def ingredienteListBoxSelect(self, event):
		widget = event.widget
		selection = widget.curselection()[0]
		value = self.ingredientes[selection]
		self.idIngrediente.set(value.idIngrediente)
		self.nombreIngrediente.set(value.nombre)

	def populatePlatillos(self):
		self.platillos = self.sistema.platillosDB.buscarTodos()
		for p in self.platillos:
			self.platillosListbox.insert(tk.END, str(p))

	def populateIngredientesPlatillo(self, idPlatillo):
		self.ingredientePlatillos = self.sistema.ingredientesDB.buscarIngredientesFromPlatillo(idPlatillo)
		for ip in self.ingredientePlatillos:
			self.ingredientesPlatilloListbox.insert(tk.END, str(ip))

	def populateIngredientes(self):
		self.ingredientes = self.sistema.ingredientesDB.buscarTodos()
		for i in self.ingredientes:
			self.ingredienteListbox.insert(tk.END, str(i))

	def cls(self):
		self.idPlatillo.set("")
		self.nombre.set("")
		self.precio.set("")
		self.categoria.set("")
		self.plugin.set("")

	def insertarPlatillo(self):
		if self.nombre.get() == "" or self.precio.get() == "" or self.categoria.get() == "":
			mb.showinfo("Warning", "¡Faltan datos!", parent=self.master)
			return

		answer = mb.askquestion("Insertar", "¿Son correctos los datos?", icon="warning", parent=self.master)
		nuevoPlatillo = Platillo(self.nombre.get(), self.precio.get(), self.categoria.get(), pluginName=self.plugin.get())
		if answer == "yes":
			try:
				self.sistema.platillosDB.insertar(nuevoPlatillo)
				self.sistema.platillosDB.confirmar()
			except Exception as err:
				mb.showinfo("error", str(err))
				self.sistema.escribirError(err)
				return
		clearListbox(self.platillosListbox)
		self.populatePlatillos()

	def borrarPlatillo(self):
		"""
		Función para el botón de borrar que funciona de la siguiente manera:
		Se ingresará únicamente el ID, lo demás será ignorado. Se borrará el cliente con este ID.
		"""
		if self.idPlatillo.get() == "":
			mb.showinfo("Advertencia", "¡Se debe ingresar un ID!", parent=self.master)
			return
		self.busqueda(self.idPlatillo.get())
		if self.idPlatillo.get() == "¡ERROR! No se encontró información":
			mb.showinfo("¡Error!", "No se encontraron coincidencias. No se continuará con el proceso.", parent=self.master)
			self.cls()
			return
		answer = mb.askquestion("Borrar", "Los datos se perderán permanentemente. Favor de revisar.", parent=self.master)
		if answer == "yes":
			try:
				self.sistema.platillosDB.borrar(self.idPlatillo.get())
				self.sistema.platillosDB.confirmar()
			except Exception as err:
				mb.showinfo("Error", sys.exc_info()[0])
				self.sistema.escribirError(err)
				return
			self.cls()
			clearListbox(self.platillosListbox)
			self.populatePlatillos()

	def showMain(self):
		"""
		Se retorna a la ventana padre.
		"""
		self.master.destroy()

	def busqueda(self, identificador=""):
		"""
		Función para el botón de Buscar que funciona de la siguiente manera:
		En esta función si se envía como argumento el identificador se utilizará este ID
		para hacer la busqueda. De no ser así se hará el busqueda con la siguiente jerarquía:
			id -> nick -> correo -> nombre
		Es decir que si no se tiene escrito el id en su campo se buscará por nick y así sucesivamente.
		"""
		try:
			if identificador:
				query = self.sistema.platillosDB.buscarID(identificador)
			elif self.idPlatillo.get():
				query = self.sistema.platillosDB.buscarID(int(self.idPlatillo.get()))
			else:
				mb.showinfo("Error", "No se ingresaron datos", parent=self.master)
				return
		except ValueError as err:
			mb.showerror("Dato incorrecto", "Favor de escribir un número")
			return

		self.idPlatillo.set(query.idPlatillo)
		self.nombre.set(query.nombre)
		self.categoria.set(query.categoria)
		self.precio.set(query.precio)

	def actualizarPlatillo(self):
		updateValue = dict()
		if not self.idPlatillo.get():
			return
		query = self.sistema.platillosDB.buscarID(int(self.idPlatillo.get()))
		if self.nombre.get() and self.nombre.get() != query.nombre:
			updateValue["nombre"] = self.nombre.get()

		if self.precio.get() and self.precio.get() != str(query.precio):
			updateValue["precio"] = self.precio.get()

		if self.categoria.get() and self.categoria.get() != query.categoria:
			updateValue["categoria"] = self.categoria.get()

		if self.plugin.get() and self.plugin.get() != query.pluginName:
			updateValue["plugin"] = self.plugin.get()

		if self.sistema.platillosDB.actualizar(self.idPlatillo.get(), **updateValue):
			self.sistema.platillosDB.confirmar()
			clearListbox(self.platillosListbox)
			self.populatePlatillos()
			self.cls()

	def platillosfromCSV(self):
		filePath = fd.askopenfilename(parent=self.master)
		if filePath:
			if mb.askokcancel(title="Alerta", message="Se borrarán todos los datos de los platillos existentes. ¿Está seguro de continuar?"):
				if self.sistema.cargarPlatillosDesdeCsv(filePath):
					self.sistema.platillosDB.confirmar()
					clearListbox(self.platillosListbox)
					self.populatePlatillos()
					self.cls()
					mb.showinfo(title="Éxito", message="La operación se realizó exitosamente")
				else:
					mb.showwarning(title="Error", message="No se pudo leer el archivo, se restauraron los datos anteriores.")

	def ingredientesfromCSV(self):
		filePath = fd.askopenfilename(parent=self.master)
		if filePath:
			if mb.askokcancel(title="Alerta", message="Se borrarán todos los datos de los ingredientes existentes. ¿Está seguro de continuar?"):
				if self.sistema.cargarIngredientesDesdeCsv(filePath):
					self.sistema.ingredientesDB.confirmar()
					clearListbox(self.ingredienteListbox)
					self.populateIngredientes()
					mb.showinfo(title="Éxito", message="La operación se realizó exitosamente")
				else:
					mb.showwarning(title="Error", message="No se pudo leer el archivo, se restauraron los datos anteriores.")



if __name__ == '__main__':
	root = tk.Tk()
	app = Instanciador(master=root)
	root.protocol("WM_DELETE_WINDOW", app.onCloseWindow)
	app.mainloop()

