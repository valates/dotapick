""" For an inputted string HERONAME, formats the string to represent the actual hero's name. 
	The formatted string is returned. """
def properFormatName(heroname):
	properHero = ''
	for i in range(0, len(heroname)):
		if ((i == 0) or (heroname[(i - 1)] == ' ') or (heroname[(i - 1)] == '-')):
			properHero += heroname[i].capitalize()
		else:
			properHero += heroname[i]
	properHero = properHero.replace("Of", "of")
	properHero = properHero.replace("The", "the")
	return prophetFix(properHero)

""" For an inputted string HERONAME, fixes an edge case where the
	associated heroname after being stored in a Tuple changes from
	"Nature's" to "Natures". The updated string is returned. """
def prophetFix(heroname):
	return heroname.replace("Natures", "Nature's")