import datetime

class MainSystem():
	def __init__(self):
		fecha = datetime.datetime.now()
		self.dia = str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year)
		self.reporteCadena = ""
		self.dineroCaja = ""
		with open("Comandas\\" + self.dia + ".csv", "a+") as arch:
			if (arch.tell() == 0):
				arch.write("hora,#Clientes,total,propina,total + propina,dineroRecibido,cambio")

	def nuevaComanda(self, numClientes, total, dineroRecibido, propina=0, tarjeta=False):
		self.error = False
		try:
			if tarjeta:
				dineroRecibido="0"
			self.comanda = Comanda(int(numClientes), int(total), int(dineroRecibido), int(propina), tarjeta)
		except ValueError:
			self.error = True

	def nuevaPropina(self, propina):
		self.comanda.propina = int(propina)

	def commitComanda(self):
		temp = str(datetime.datetime.now().time())
		with open("Comandas\\" + self.dia + ".csv", "a") as arch:
			arch.write("\n" + temp[:temp.index(".")] + "," + str(self.comanda))

	def calculoComanda(self, con, string=False):
		total = sum(con)
		if string:
			return "Total: " + str(total) + "\nPropina Sugerida: " + str(int(total * 0.1)) + "\nTotal Sugerido: " + str(int(total * 1.1))
		return {"Total":str(total), "Propina":str(int(total*0.1)), "Sugerido": str(int(total * 1.1))}

	def cierreDeCaja(self, dineroCaja, dineroInicial, gastos, nomina,prestamos="", dia=""):
		self.dineroCaja = int(dineroCaja)
		self.reporteCadena = ""
		totalClientes = 0
		ventasEfectivo = 0
		ventasTarjeta = 0
		
		totalPropinaEfectivo = 0
		totalPropinaTarjeta = 0
		totalVentasPropina = 0
		totalMesas = 0
		dineroInicial = int(dineroInicial)
		if dia == "":
			diaFunc = self.dia
		else:
			diaFunc = dia
		diaFunc = [x.lstrip("0") for x in diaFunc.split("-")]
		if gastos == "":
			gastos = 0
		else:
			gastos = int(gastos)

		if nomina == "":
			nomina = 0
		else:
			nomina = int(nomina)

		if prestamos == "":
			prestamos = 0
		else:
			prestamos = int(prestamos)
		try:
			with open("Comandas\\" + str(diaFunc[0]) + "-" + str(diaFunc[1]) + "-" + str(diaFunc[2]) + ".csv", "r") as arch:
				#Leemos todos los datos recopilados del día.
				for line in arch:
					if not line.startswith("hora") and not (line + " ").isspace():
						line = line.split(",")
						totalMesas += 1
						totalClientes += int(line[1])
						if line[-1].rstrip("\n") == "TARJETA":
							ventasTarjeta += int(line[2])
							totalPropinaTarjeta += int(line[3])
						else:
							ventasEfectivo += int(line[2])
							totalPropinaEfectivo += int(line[3])
						totalVentasPropina += int(line[4])
		except FileNotFoundError:
			return "Archivo no encontrado " + str(diaFunc[0]) + "-" + str(diaFunc[1]) + "-" + str(diaFunc[2]) + ".csv"
		
		neto = dineroInicial + ventasEfectivo - gastos - nomina - totalPropinaTarjeta
		netoEfectivo = self.dineroCaja - nomina - totalPropinaTarjeta
		diffDinero = netoEfectivo - neto

		self.reporteCadena = str(diaFunc[0]) + "-" + str(diaFunc[1]) + "," + str(totalMesas) + "," + str(totalClientes) + "," +\
		str(dineroInicial) + "," + str(ventasEfectivo) + "," + str(ventasTarjeta) + "," + str(gastos) + "," +\
		str(nomina) + "," + str(neto) + "," + str(self.dineroCaja) + "," + str(diffDinero)

		self.totalPropinas = totalPropinaTarjeta + totalPropinaEfectivo
		return (self.reporteCadena, self.totalPropinas)

	def commitCierre(self, llevo, dia=""):
		if dia == "":
			diaFunc = self.dia
		else:
			diaFunc = dia
		diaFunc = [x.lstrip("0") for x in diaFunc.split("-")]
		try:
			with open("Reportes\\Reporte" + diaFunc[1] + "_" + diaFunc[2] + ".csv","a") as reporte:
				if reporte.tell() == 0:
					reporte.write("Dia,Total Mesas,Total Clientes,Caja,Cobro Efectivo,Terminal,Gastos,Sueldo,Neto,Dinero,Sobra/Falta,Llevo,Dejo,Propinas\n")
				self.reporteCadena += "," + llevo + "," + str(int(self.dineroCaja) - int(llevo)) + "," + str(self.totalPropinas) + "\n"
				reporte.write(self.reporteCadena)
		except PermissionError:
			print("Favor de cerrar el archivo del reporte")

	def __bool__(self):
		return self.error

class Comanda(object):
	"""
	TODO:
		Eventualmente sería bueno agregarle consumo para que se puedan tener varias comandas al mismo tiempo	
	"""
	def __init__(self, numClientes, total, dineroRecibido, propina, tarjeta=False):
		self.numClientes = numClientes
		self.total = total
		self.propina = propina
		self.dineroRecibido = dineroRecibido
		self.tarjeta = tarjeta

	def agregarPropina(self, propina=0):
		self.propina += propina

	def cobro(self):
		if self.tarjeta:
			return "Num. Clientes: " + str(self.numClientes) + "\nTotal: " + str(self.total) + "\nPropina: " + str(self.propina) +\
		 	"\nTotal con Propina: " + str(self.total + self.propina) + "\nPAGO CON TARJETA"
		return "Num. Clientes: " + str(self.numClientes) + "\nTotal: " + str(self.total) + "\nPropina: " + str(self.propina) +\
		 "\nTotal con Propina: " + str(self.total + self.propina) + "\nDinero Recibido: " + str(self.dineroRecibido) +\
		 "\nCambio: " + str(self.dineroRecibido - self.propina - self.total)

	def __str__(self):
		""" Formato: #Clientes, total, propina, total + propina, dineroRecibido, cambio """
		if self.tarjeta:
			return str(self.numClientes) + "," + str(self.total) + "," + \
		 str(self.propina) + "," + str(self.propina + self.total)  + "," + \
		 "TARJETA" + ",TARJETA" 

		return str(self.numClientes) + "," + str(self.total) + "," + \
		 str(self.propina) + "," + str(self.propina + self.total)  + "," + \
		 str(self.dineroRecibido) + "," + str(self.dineroRecibido - self.propina - self.total)

if __name__ == '__main__':
	print("Porfavor abir TeruGUI")
	sistema = MainSystem()
	sistema.cierreDeCaja("1234", "12", "2", "20")