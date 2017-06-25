def parseFloat(val):
	if type(val) is str:
		if val.endswith("."):
			val+="0"
	return float(val)