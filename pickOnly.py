import sys, fileOperators, nameFormater, constantNames, shorthand, pickleSerializers, htmlOperators
from fileOperators import *
from nameFormater import *
from constantNames import *
from shorthand import *
from pickleSerializers import *
from htmlOperators import htmlSearcher, htmlSearchAll

#TODO help option output from file contents
#TODO comment functions

#kotl pick not work after zeus, huskar


HEROES_LIST = splitFileByNewline(HERONAME_FILE)

def main(args):
	argc = len(sys.argv)
	argv = sys.argv
	percentThreshold = 2.0
	if (argc == 2):
		if (argv[1].lower() == "--formathtml"):
			formatAdv()
		if (argv[1].lower() == "--reset"):
			resetShorthands()
			print("Shorthands reset. Printing resulting dictionary: ")
			print(load_obj(SHORTHAND_PICKLE_NAME))
	elif ((argc == 4) and (argv[1].lower() == "--addshort")):
		addShorthand(properFormatName(argv[2]), argv[3], shortDict)
	else:
		if ((argc == 3) and (argv[1].lower() == "setpercent")):
			percentThreshold = float(argv[2])
		startPicks(percentThreshold)

def formatAdv():
	heroLen = len(HEROES_LIST)
	heroHtml = splitFileByNewline("data/herohtml")
	heroAdvDict = {}
	dataStart = "<table class=\"sortable\">"
	dataEnd = "</table>"
	advStart = "<td class=\"cell-xlarge\">"
	advCutoff = "<div class=\"bar bar-default\"><div class=\"segment segment-advantage\""
	for hero in HEROES_LIST:
		urlText = heroHtml.pop(0)
		if (urlText):
			searchBlock = htmlSearcher(dataStart, dataEnd, urlText, False, True)[0]
			advantages = htmlSearchAll(advStart, advCutoff, searchBlock)
			advBlock = []
			for entry in advantages:
				entryName = entry[:-5]
				entryPercent = entry[-5:-1]
				if (entryName[-1] == '-'):
					entryName = entryName[:-1]
					entryPercent = '-' + entryPercent
				entryTuple = (entryName, entryPercent)
				advBlock.append(entryTuple)
			heroAdvDict[hero] = advBlock
		print('{:<20}'.format(hero) + "\t" + str(heroLen - len(heroHtml)) + "/" + str(heroLen))
	save_obj(heroAdvDict, ADV_PICKLE_NAME)
	formShorthands()

def startPicks(percentThreshold):
	heroAdvantageDict = load_obj(ADV_PICKLE_NAME)
	shortDict = load_obj(SHORTHAND_PICKLE_NAME)
	heroAdvMap = {}
	heroesLeft = []
	pickedHeroes = []
	for hero in HEROES_LIST:
		heroAdvMap[hero] = []
		heroesLeft.append(hero)
	outputHeroesLeft(heroesLeft, heroAdvMap)
	while (len(pickedHeroes) < 5):
			print("\n")
			pickedHero = input("Enter picked hero, 'sort,' to sort current, or 'q' to quit: ").lower()
			if (pickedHero == KILL_COMMAND):
				exit()
			elif (pickedHero in SORT_INPUTS):
				print("Not currently in sorting function. Entry 'sort' to switch.")
			elif (pickedHero == "sort"):
				if (len(pickedHeroes) == 0):
					print("Cannot sort without any advantages. Pick a hero first.")
				else:
					performSort(heroesLeft, heroAdvMap, pickedHeroes)
			elif(pickedHero[:3].lower() == BAN_COMMAND):
				if (pickedHero in shortDict):
					pickedHero = shortDict[pickedHero]
				else:
					pickedHero = properFormatName(pickedHero[4:])
				heroesLeft.remove(pickedHero)
				print(pickedHero + " banned.")
				outputHeroesLeft(heroesLeft, heroAdvMap)
			else:
				if (pickedHero in shortDict):
					properHero = shortDict[pickedHero]
				else:
					properHero = properFormatName(pickedHero)
				if (properHero in HEROES_LIST):
					properHero, pickedHeroes, heroesLeft, heroAdvantageDict, heroAdvMap = performAdvantageSearch(properHero, 
																												pickedHeroes, 
																												heroesLeft, 
																												heroAdvantageDict, 
																												heroAdvMap, 
																												percentThreshold)
				else:	
					print("Invalid hero name '" + pickedHero + "', add it to shorthands?")
					heroToMap = properFormatName(input("If so, enter a valid hero name: "))
					if heroToMap in HEROES_LIST:
						response = input("Adding shorthand '" + pickedHero + "' for hero '" + heroToMap + "'. Enter 'y' to confirm: ")
						if (response == 'y'):
							addShorthand(heroToMap, pickedHero, shortDict)
							print("Shorthand added.")
						else:
							print("Shorthand cancelled.")
						response = input("Enter 'y' to pick " + heroToMap + ": ")
						if (response == 'y'):
							properHero = heroToMap
							properHero, pickedHeroes, heroesLeft, heroAdvantageDict, heroAdvMap = performAdvantageSearch(properHero, 
																														pickedHeroes, 
																														heroesLeft, 
																														heroAdvantageDict, 
																														heroAdvMap, 
																														percentThreshold)
					else:
						print("Invalid hero name '" + heroToMap + "', not adding to shorthands. Please enter a real name.")
	performSort(heroesLeft, heroAdvMap, pickedHeroes)

def performAdvantageSearch(properHero, pickedHeroes, heroesLeft, heroAdvantageDict, heroAdvMap, percentThreshold):
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
		pickedHeader = ''
		for hero in pickedHeroes:
			pickedHeader += '{:^20}'.format(hero)
		print('{:<20}'.format("Hero") + pickedHeader)
		outputHeroesLeft(heroesLeft, heroAdvMap)
	else:
		print("Hero already marked as picked.")
	print("\n\nPicked heroes:")
	for hero in pickedHeroes:
		print(hero)
	return properHero, pickedHeroes, heroesLeft, heroAdvantageDict, heroAdvMap

def outputHeroesLeft(heroesLeft, heroAdvMap):
	for hero in heroesLeft:
		heroDisplay = '{:<20}'.format(hero)
		advStats = ''
		for adv in heroAdvMap[hero]:
			advStats += '{:^20}'.format(adv) + "\t"
		print(heroDisplay + "\t" + advStats)
	print(str(len(heroesLeft)) + " heroes remaining.")

def performSort(heroesLeft, heroAdvMap, pickedHeroes):
	while (True):
		print("Enter " + KILL_COMMAND + " at any time to quit sorting.")
		sortOption = input("\n\nEnter sorting method (" + SORT_INPUTS[0] + ", " + SORT_INPUTS[1] + ", or 1-5): ").lower()
		if (sortOption == KILL_COMMAND):
			break
		sortValues = []
		for hero in heroesLeft:
			heroAdvantages = heroAdvMap[hero]
			heroTuple = (hero, heroAdvantages)
			sortValues.append(heroTuple)
		if (sortOption in SORT_INPUTS[:2]):
			sumList = []
			for entry in sortValues:
				entryName = entry[0]
				entryList = entry[1]
				entrySum = 0
				for value in entryList:
					entrySum += value
				if (sortOption == SORT_INPUTS[1]):
					entrySum /= len(pickedHeroes)
				sumTuple = (entryName, entrySum)
				sumList.append(sumTuple)
			sumList = sorted(sumList, key=lambda curSum: curSum[1])
			for sumEntry in sumList:
				heroDisplay = '{:<20}'.format(sumEntry[0]) + '\t' + '{0:.2f}'.format(sumEntry[1])
				print(heroDisplay)
		else:
			if (sortOption in SORT_INPUTS[2:]):
				sortOption = int(sortOption)
				if (sortOption <= len(pickedHeroes)):
					sortValues = sorted(sortValues, key=lambda curList: (curList[1])[(sortOption - 1)])
					pickedHeader = ''
					for hero in pickedHeroes:
						pickedHeader += '{:<20}'.format(hero)
					print('{:<20}'.format("Hero") + pickedHeader)
					for sortEntry in sortValues:
						heroDisplay = '{:<20}'.format(sortEntry[0])
						advStats = ''
						for adv in sortEntry[1]:
							advStats += '{:>20}'.format(adv) + "\t"
						print(heroDisplay + "\t" + advStats)
				else:
					print("Insufficient number of picked heroes to sort by column '" + str(sortOption) + "'")
			else:
				print("Invalid sorting column '" + sortOption + "'")

if __name__ == '__main__':
    main(sys.argv)