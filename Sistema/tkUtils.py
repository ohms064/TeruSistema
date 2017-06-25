import tkinter as tk

def updateListbox(listbox, index, value):
	listbox.delete(index)
	listbox.insert(index, value)

def validate(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type):

	if text in '0123456789.-+' or not text:
		try:
			float(value_if_allowed)
			return True
		except ValueError:
		    return False
	else:
	    return False

def checkVar(tkVar, default):
	if not tkVar.get():
		tkVar.set(default)
		return True
	return False

def clearListbox(listbox):
	listbox.delete(0, tk.END)

def createListbox(master, width=65, height=10):
	frame = tk.Frame(master)
	scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
	customFont = tk.font.Font(family="Monaco", size=8)
	listbox = tk.Listbox(frame, width=width, height=height, yscrollcommand=scrollbar.set, font=customFont, exportselection=False)
	scrollbar.config(command=listbox.yview)
	scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
	listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
	return frame, listbox