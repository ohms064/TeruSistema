def updateListbox(listbox, index, value):
	listbox.delete(index)
	listbox.insert(index, value)