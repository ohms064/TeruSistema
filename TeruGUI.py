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
		texto = dict()
		self.strVar = dict()

		self.strVar["Clientes"] = tk.StringVar()
		self.strVar["Recibido"] = tk.StringVar()
		self.strVar["Propina"] = tk.StringVar()
		self.strVar["Total"] = tk.StringVar()

		etiquetas["Clientes"] = tk.Label(self.master, text="Clientes:").place(x=50, y=10)
		texto["Clientes"] = tk.Entry(self.master, textvariable=self.strVar["Clientes"]).place(x=110, y=10)

		etiquetas["Propina"] = tk.Label(self.master, text="Propina:").place(x=50, y=30)
		texto["Propina"] = tk.Entry(self.master, textvariable=self.strVar["Propina"]).place(x=110, y=30)

		etiquetas["Total"] = tk.Label(self.master, text="Total:").place(x=65, y=50)
		texto["Total"] = tk.Entry(self.master, textvariable=self.strVar["Total"]).place(x=110, y=50)

		etiquetas["Recibido"] = tk.Label(self.master, text="Dinero recibido:").place(x=10, y=70)
		texto["Recibido"] = tk.Entry(self.master, textvariable=self.strVar["Recibido"]).place(x=110, y=70)

		etiquetas["Consumo"] = tk.Label(self.master, text="Consumo:").place(x=40, y=130)
		texto["Consumo"] = tk.Text(self.master, width=24, height=5).place(x=110, y=130)
		butCalcular = tk.Button(self.master, text="Sumar").place(x=260, y=220)

		butAceptar = tk.Button(self.master, text="Aceptar", command=self.callSystem).place(x=185,y=95)

	def callSystem(self):
		self.sistema.nuevaComanda(self.strVar["Clientes"].get(), self.strVar["Total"].get(), self.strVar["Recibido"].get(), self.strVar["Propina"].get())
		newWindow = tk.Toplevel(self)
		newWindow.wm_title("Comanda")
		recibo = tk.Label(newWindow, text=self.sistema.comanda.cobro()).place(x=10,y=10)

root = tk.Tk()
app = MainGUI(master=root)
app.mainloop()