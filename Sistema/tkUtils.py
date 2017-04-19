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

class tkCustomWindow:
	def __init__(self):
		pass