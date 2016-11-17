from constantNames import HEROES_LIST
from sorting import performSort
from shorthand import addShorthand
from nameFormater import properFormatName
from fileOperators import splitFileByNewline
from nameFormater import prophetFix
from pythonShortcomings import iterateAndRemove

def initHeroAdvs():
	heroAdvMap, heroesLeft = {}, []
	for hero in HEROES_LIST:
		heroAdvMap[hero] = []
		heroesLeft.append(hero)
	return heroAdvMap, heroesLeft

def findHero(pickedHero, shortDict, heroesToCheckForPick):
	if ((pickedHero in shortDict) or (pickedHero.lower() in shortDict)):
		properHero = shortDict[pickedHero]
	else:
		properHero = properFormatName(pickedHero)
	if (properHero not in HEROES_LIST):
		properHero, shortDict = addToShorthands(pickedHero, shortDict)
	if ((heroesToCheckForPick != HEROES_LIST) and (properHero not in heroesToCheckForPick)):
		return None, shortDict
	return properHero, shortDict

def pickHero(pickedHero, shortDict, pickedHeroes, heroesLeft, heroAdvantageDict, heroAdvMap, percentThreshold, sortPrefix):
	properHero, shortDict = findHero(pickedHero, shortDict, HEROES_LIST)
	if (properHero is not None):
		pickedHeroes, heroesLeft, heroAdvMap = performAdvantageSearch(properHero, 
																	  pickedHeroes, 
																	  heroesLeft, 
																	  heroAdvantageDict, 
																	  heroAdvMap, 
																	  percentThreshold, 
																	  sortPrefix)
	return pickedHeroes, heroesLeft, heroAdvMap, shortDict

def banHero(pickedHero, shortDict, heroesLeft, heroAdvMap, pickedHeroes, sortPrefix):
	properHero, shortDict = findHero(pickedHero[3:].strip(), shortDict, heroesLeft)
	if (properHero is not None):
		heroesLeft.remove(properHero)
		print(pickedHero + " banned.")
		performSort(heroesLeft, heroAdvMap, pickedHeroes, sortPrefix)
	else:
		print("'" + pickedHero + "' not present in hero list. Try again.")
	return heroesLeft

def undoPick(properHero, pickedHeroes, heroesLeft, heroAdvantageDict, heroAdvMap, percentThreshold, sortPrefix):
	pickedHeroes.remove(properHero)
	heroAdvMap, heroesLeft = initHeroAdvs()
	pickedCopy = []
	for hero in pickedHeroes:
		pickedCopy, heroesLeft, heroAdvMap = performAdvantageSearch(hero, 
																	pickedCopy, 
																	heroesLeft, 
																	heroAdvantageDict, 
																	heroAdvMap, 
																	percentThreshold, 
																	sortPrefix)
	return pickedCopy, heroesLeft, heroAdvMap

def focusRemainingHeroPool(focusSpecifier, heroesLeft, heroAdvMap, pickedHeroes, sortPrefix):
	toFocus = splitFileByNewline("data/" + focusSpecifier)
	heroesLeft = iterateAndRemove(heroesLeft, lambda toFocus, entry: entry not in toFocus, toFocus)
	performSort(heroesLeft, heroAdvMap, pickedHeroes, sortPrefix)
	return heroesLeft

def performAdvantageSearch(properHero, pickedHeroes, heroesLeft, heroAdvantageDict, heroAdvMap, percentThreshold, sortPrefix):
	print("\n**********\n")
	if (properHero not in pickedHeroes):
		if properHero in heroesLeft:
			heroesLeft.remove(properHero)
		heroAdvs = heroAdvantageDict[properHero]
		for entryTuple in heroAdvs:
			entryName = entryTuple[0]
			entryName = prophetFix(entryName)
			entryAdv = float(entryTuple[1])
			heroAdvMap[entryName].append(entryAdv)
			if (entryAdv > percentThreshold):
				if (entryName in heroesLeft):
					heroesLeft.remove(entryName)
		pickedHeroes.append(properHero)
		performSort(heroesLeft, heroAdvMap, pickedHeroes, sortPrefix)
	else:
		print("Hero already marked as picked.")
	print("\n\nPicked heroes:")
	for hero in pickedHeroes:
		print(hero)
	return pickedHeroes, heroesLeft, heroAdvMap

def addToShorthands(pickedHero, shortDict):
	heroToReturn = None
	print("Invalid hero name '" + pickedHero + "', add it to shorthands?")
	heroToMap = properFormatName(input("If so, enter a valid hero name: "))
	heroToMap, shortDict = findHero(heroToMap, shortDict, HEROES_LIST)
	if (heroToMap is not None):
		response = input("Adding shorthand '" + pickedHero + "' for hero '" + heroToMap + "'. Enter 'y' to confirm: ")
		if (response == 'y'):
			shortDict = addShorthand(heroToMap, pickedHero, shortDict)
			heroToReturn = heroToMap
	else:
		print("Invalid hero name '" + heroToMap + "', not adding to shorthands. Please enter a real name.")
	return heroToReturn, shortDict