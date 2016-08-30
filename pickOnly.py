import sys, os
from os import remove, rename

HERONAME_FILE = 'heroes.txt'
MATCHES_FILE = 'heromatch.txt'
SHORTHAND_FILE = 'shorthands.txt'
DUPLICATE_FILE = 'duplicates.txt'
TEMP_NAME = 'tmp.txt'

def splitFileByNewline(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    return lines

HEROES_LIST = splitFileByNewline(HERONAME_FILE)
SORT_INPUTS = ['sum', 'average', '1', '2', '3', '4', '5']
KILL_COMMAND = 'q'
""" Makes no sense to add a shorthand for every single hero. """
KILL_ALL = '*'
SHORTHAND_BLACKLIST = [KILL_ALL]

def main(args):
    argc = len(sys.argv)
    argv = sys.argv[1:]
    percentThreshold = 2.0
    if (argc == 2):
    	percentThreshold = float(argv[0])
    startPicks(percentThreshold)

def startPicks(percentThreshold):
	matchupData = splitFileByNewline(MATCHES_FILE)
	heroDict = {}
	heroAdvMap = {}
	heroCount = 0
	heroesLeft = []
	for hero in HEROES_LIST:
		heroDict[hero] = heroCount
		heroAdvMap[hero] = []
		heroesLeft.append(hero)
		heroCount += 1
	pickedHeroes = []
	outputHeroesLeft(heroesLeft, heroAdvMap)
	dups = formDuplicates()
	shorts = formShorthands(dups[1])
	shorthandDict = shorts[1]
	while (len(pickedHeroes) < 5):
		try:
			print("\n")
			pickedHero = input("Enter picked hero, \"sort\" to sort current, or \"" + KILL_COMMAND + "\" to quit: ").lower()
			if (pickedHero == KILL_COMMAND):
				exit()
			elif (pickedHero in SORT_INPUTS):
				print("Not currently in sorting function. Entry 'sort' to switch.")
			elif (pickedHero == "sort"):
				if (len(pickedHeroes) == 0):
					print("Cannot sort without any advantages. Pick a hero first.")
				else:
					performSort(heroesLeft, heroAdvMap, pickedHeroes)
			else:
				if (pickedHero in shorthandDict):
					properHero = shorthandDict[pickedHero]
				else:
					properHero = properFormatName(pickedHero)
				print("\n**********\n")
				if (properHero not in pickedHeroes):
					if properHero in heroesLeft:
						heroesLeft.remove(properHero)
					heroAdvs = matchupData[heroDict[properHero]]
					heroAdvs = heroAdvs[1:-1]
					heroAdvs = heroAdvs.split('), ')
					for entry in heroAdvs:
						entry = entry[1:]
						entry = entry.replace('\'', '')
						entry = entry.replace('\"', '')
						entryTuple = entry.split(', ')
						entryName = entryTuple[0]
						entryName = prophetFix(entryName)
						entryTuple[1] = entryTuple[1].replace(')', '')
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
		except KeyError:
			print("Invalid hero name '" + pickedHero + "', add it to shorthands?")
			heroToMap = properFormatName(input("If so, enter a valid hero name: "))
			if heroToMap in heroDict:
				response = input("Adding shorthand '" + pickedHero + "' for hero '" + heroToMap + "'. Enter 'y' to confirm: ")
				if (response == 'y'):
					addShorthand(heroToMap, pickedHero, shorts[0])
					shorthandDict[pickedHero] = heroToMap
					print("Shorthand added.")
				else:
					print("Shorthand cancelled.")
				response = input("Enter 'y' to pick '" + heroToMap + "': ")
				if (response == 'y'):
					#Find a more efficient approach to this...
					properHero = heroToMap
					print("\n**********\n")
					if (properHero not in pickedHeroes):
						if properHero in heroesLeft:
							heroesLeft.remove(properHero)
						heroAdvs = matchupData[heroDict[properHero]]
						heroAdvs = heroAdvs[1:-1]
						heroAdvs = heroAdvs.split('), ')
						for entry in heroAdvs:
							entry = entry[1:]
							entry = entry.replace('\'', '')
							entry = entry.replace('\"', '')
							entryTuple = entry.split(', ')
							entryName = entryTuple[0]
							entryName = prophetFix(entryName)
							entryTuple[1] = entryTuple[1].replace(')', '')
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
			else:
				print("Invalid hero name '" + heroToMap + "', not adding to shorthands. Please enter a real name.")
	performSort(heroesLeft, heroAdvMap, pickedHeroes)

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
					entrySum /= 5
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
						heroDisplay = '{:^20}'.format(sortEntry[0])
						advStats = ''
						for adv in sortEntry[1]:
							advStats += '{:>20}'.format(adv) + "\t"
						print(heroDisplay + "\t" + advStats)
				else:
					print("Insufficient number of picked heroes to sort by column '" + str(sortOption) + "'")
			else:
				print("Invalid sorting column '" + sortOption + "'")

def updateFile(lines, filename):
	tmpFile = open(TEMP_NAME, 'w')
	for line in lines:
		tmpFile.write((line + '\n'))
	tmpFile.close()
	os.remove(filename)
	os.rename(TEMP_NAME, filename)

def formDictFromCommaFile(filename, duplicates = {}):
	lines = splitFileByNewline(filename)
	commaLists = []
	for line in lines:
		lineList = line.split(', ')
		if (len(lineList) != 1):
			commaLists.append(lineList)
	curDict = {}
	for entry in commaLists:
		listKeys = entry[1:]
		listVal = entry[0]
		for curKey in listKeys:
			if curKey not in duplicates:
				curDict[curKey] = listVal
	return (lines, curDict)

def formDuplicates():
	return formDictFromCommaFile(DUPLICATE_FILE)

def formShorthands(duplicatesDict):
	return formDictFromCommaFile(SHORTHAND_FILE, duplicatesDict)

def addShorthand(heroname, shorthand, shorthandLines):
	newLines = []
	for line in shorthandLines:
		lineSplit = line.split(', ')
		name = lineSplit[0]
		values = lineSplit[1:]
		newline = name
		if ((heroname == name) and (shorthand not in values)):
			line += ", " + shorthand
		newLines.append(line)
	updateFile(newLines, SHORTHAND_FILE)
	return newLines

def addShorthands(shorthandDict, shorthandLines, heroAdvMap):
	response = 'y'
	while(response == 'y'):
		heroExist = False
		while (not heroExist):
			heroname = input("Enter heroname: ")
			if (heroname in shorthandDict):
				heroname = shorthandDict[heroname]
			else:
				heroname = properFormatName(heroname)
			heroExist = heroname in heroAdvMap
			if heroExist is False:
				print("No such hero '" + heroname + "'. Try again.")
		shorthand = input("Enter shorthand (will be forced all lowercase): ").lower()
		if (shorthand not in SHORTHAND_BLACKLIST):
			response = input("Adding shorthand '" + shorthand + "' for hero '" + heroname + "'. Enter 'y' to confirm: ")
			if (response == 'y'):
				shorthandLines = addShorthand(heroname, shorthand, shorthandLines)
				shorthandDict[shorthand] = heroname
				print(shorthandDict)
				print("Shorthand added.")
			else:
				print("Shorthand cancelled.")
		else:
			print("Sorry, that shorthand is blacklisted. Don't be naughty.")
		response = input("Enter 'y' to continue adding shorthands. Any other input to exit: ")
	return (shorthandDict, shorthandLines)

def resetShorthands(shorthandDict, shorthandLines):
	shorthandDict = {}
	shorthandLines = HEROES_LIST
	updateFile(HEROES_LIST, SHORTHAND_FILE)
	return (shorthandDict, shorthandLines)


if __name__ == '__main__':
    main(sys.argv)