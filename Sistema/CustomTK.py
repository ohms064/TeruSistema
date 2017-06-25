import tkinter as tk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import messagebox as mb
from collections import defaultdict
import datetime

class UserFormBox(tk.Frame):
	def __init__(self, master, done, textvariable=None):
		tk.Frame.__init__(self, master)
		self.Form = UserForm(self, textvariable)
		self.Form.grid(row=0, column=0)

class UserForm(tk.Frame):
	"""
	Class derived from tk.Frame that creates a form for the user to fill.
	By default the form creates a tkinter.Entry for each label but if you need another one you can pass
	a list with the desired values in listBox for dropdown lists, dateBox for dates, checkBox for check boxes and fileBox for files.
	Leave an empty string in the same place in keyLabels  and variables to create another column
	"""
	def __init__(self, master, done, rows=10, padre=None, col_size=5, keyLabels=None, dateBox=None, fileBox=None, checkBox=None, fixedValues=None, choices=None, defaultValues=None, formValues=None):
		if keyLabels is None:
			keyLabels = []
		if dateBox is None:
			dateBox = []
		if fileBox is None:
			fileBox = []
		if checkBox is None:
			checkBox = []
		if defaultValues is None:
			defaultValues = defaultdict()
		if choices is None:
			choices = defaultdict()
		if formValues is None:
			formValues = dict()

		tk.Frame.__init__(self, master)

		self.master.protocol("WM_DELETE_WINDOW", self.onCloseWindow)

		self.done = done
		self.fileBox = fileBox
		self.formValues = formValues
		self._Form(rows, col_size, keyLabels, dateBox, checkBox, defaultValues, choices)

	def onCloseWindow(self):
		self.done.set(True)
		self.formValues = {"$Cancel$":True}
		self.master.destroy()
		
	def _Form(self, rows, col_size, keyLabels, dateBox, checkBox, defaultValues, choices):
		"""
		Creates the widgets for the UserForm
		"""
		iter_row = 0 
		iter_col = 0
		max_row = -1
		for self.label in keyLabels:
			if iter_row > rows or self.label == "":
				max_row = max([iter_row, max_row])
				iter_row = 0
				iter_col += col_size
				if self.label == "":
					continue
			self.formValues[self.label] = tk.StringVar()
			tk.Label(self.master, text="{}:".format(self.label)).grid(row=iter_row, column=iter_col, sticky=tk.SE)
			if self.label in choices:
				ttk.Combobox(self.master, width=24, textvariable=self.formValues[self.label], values=choices[self.label]).grid(row=iter_row, column=iter_col + 1, columnspan=2)
				self.formValues[self.label].set(choices[self.label][0])
			
			elif self.label in dateBox:
				DateBox(self.master, textvariable=self.formValues[self.label]).grid(row=iter_row, column=iter_col + 1, sticky="ew")
			
			elif self.label in self.fileBox:
				self.formValues[self.label].set("Falta elegir: {}".format(self.label))
				tk.Button(self.master,command=self.FileDialog(self.label), text="Archivo").grid(row=iter_row, column=iter_col + 1, columnspan=4, sticky="wens")
				tk.Label(self.master,textvariable=self.formValues[self.label]).grid(row=iter_row + 1, column=iter_col, columnspan=5)
				iter_row += 1
			
			elif self.label in checkBox:
				tk.Checkbutton(self.master, variable=self.formValues[self.label], onvalue="y", offvalue="").grid(row=iter_row, column=iter_col + 1)
			
			elif self.label in defaultValues:
				self.formValues[self.label].set(defaultValues[self.label])
				tk.Entry(self.master, width=27, textvariable=self.formValues[self.label]).grid(row=iter_row, column=iter_col + 1)
			
			else:
				tk.Entry(self.master, width=27, textvariable=self.formValues[self.label]).grid(row=iter_row, column=iter_col + 1, columnspan=4)

			iter_row += 1
		max_row = max([iter_row, max_row])

		tk.Frame(self.master, borderwidth=1, width=200, height=50).grid(column=0, row=max_row+1, columnspan=3, rowspan=2)
		tk.Button(self.master, text="Aceptar", command=self.FillForm).grid(row=max_row+2, column=iter_col, columnspan=5, sticky="wens")

	def FileDialog(self, label):
		"""
		Must use a closure becouse if I use self.label it will get the last label in the list and not the corresponding label.
		"""
		def close():
			self.formValues[label].set(fd.askopenfilename(parent=self.master))
		return close

	def FillForm(self):
		for data in self.formValues:
			self.formValues[data] = self.formValues[data].get()
		for data in self.fileBox:
			if "Falta elegir: {}".format(data) == self.formValues[data]:
				self.formValues[data] = ""
		self.done.set(True)
		self.master.destroy()

class DateBox(tk.Frame):
	def __init__(self, master, textvariable=None):
		tk.Frame.__init__(self, master)
		self.chooseDate = PickDate(self, textvariable)
		self.chooseDate.grid(row=0, column=0)

class PickDate(tk.Frame):
	def __init__(self, master, textvariable=None):
		tk.Frame.__init__(self, master)
		if textvariable is None:
			self.textvariable = tk.StringVar
		else:
			self.textvariable = textvariable
		date = datetime.date.today()
		self.months = ["?","Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto", "Septiembre","Octubre","Noviembre","Diciembre"]
		#self.today = "{}-{}-{}".format(date.day, date.month, date.year)

		self.dayVar = tk.StringVar()
		self.monthVar = tk.StringVar()
		self.yearVar = tk.StringVar()

		self.dayVar.set(date.day)
		self.monthVar.set(self.months[date.month])
		self.yearVar.set(date.year)
		self.updateTextVar()

		self.dayVar.trace("w", self.updateTextVar)
		self.monthVar.trace("w", self.updateTextVar)
		self.yearVar.trace("w", self.updateTextVar)

		self.dayEntry = ttk.Combobox(self.master, textvariable=self.dayVar, values=[x for x in range(1,32)], width=2)
		self.monthEntry = ttk.Combobox(self.master, textvariable=self.monthVar, values=self.months, width=10)
		self.yearEntry = ttk.Combobox(self.master, textvariable=self.yearVar, values=[x for x in range(int(date.year) - 50, int(date.year))], width=4)

		self.dayEntry.grid(column=1, row=0)
		self.monthEntry.grid(column=2, row=0)
		self.yearEntry.grid(column=3, row=0)
	
	def updateTextVar(self, *args, **kwargs):
		self.textvariable.set("{}-{}-{}".format(self.dayVar.get(), self.monthVar.get(), self.yearVar.get()))