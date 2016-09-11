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

def prophetFix(heroname):
	return heroname.replace("Natures", "Nature's")