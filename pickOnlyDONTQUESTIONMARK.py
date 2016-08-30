import sys

def splitFileByNewline(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    return lines

HEROES_LIST = splitFileByNewline("heroes.txt")
SORT_INPUTS = ['sum', 'average', '1', '2', '3', '4', '5']
KILL_COMMAND = 'q'

def main(args):
    argc = len(sys.argv)
    argv = sys.argv[1:]
    percentThreshold = 2
    if (argc == 2):
    	percentThreshold = float(argv[0])
    startPicks(percentThreshold)

def startPicks(percentThreshold):
	matchupData = splitFileByNewline("heromatch.txt")
	heroDict = {}
	heroAdvMap = {}
	heroCount = 0
	heroesLeft = []
	for hero in HEROES_LIST:
		heroDict[hero.lower()] = heroCount
		heroAdvMap[hero.lower()] = []
		heroesLeft.append(hero)
		heroCount += 1
	pickedHeroes = []
	outputHeroesLeft(heroesLeft, heroAdvMap)
	while (len(pickedHeroes) < 5):
		try:
			print("\n")
			pickedHero = input("Enter picked hero, \"sort\" to sort current, or \"" + KILL_COMMAND + "\" to quit: ")
			if (pickedHero.lower() == KILL_COMMAND):
				exit()
			elif (pickedHero.lower() in SORT_INPUTS):
				print("Not currently in sorting function. Entry 'sort' to switch.")
			elif (pickedHero.lower() == "sort"):
				if (len(pickedHeroes) == 0):
					print("Cannot sort without any advantages. Pick a hero first.")
				else:
					performSort(heroesLeft, heroAdvMap, pickedHeroes)
			else:
				pickedHero = prophetFix(pickedHero).lower()
				print("\n**********\n") 
				if (pickedHero not in pickedHeroes):
					properHero = properFormatName(pickedHero)
					if properHero in heroesLeft:
						heroesLeft.remove(properHero)
					heroAdvs = matchupData[heroDict[pickedHero]]
					heroAdvs = heroAdvs[1:-1]
					heroAdvs = heroAdvs.split('), ')
					for entry in heroAdvs:
						entry = entry[1:]
						entry = entry.replace('\'', '')
						entryTuple = entry.split(', ')
						entryName = entryTuple[0]
						entryName = prophetFix(entryName)
						entryTuple[1] = entryTuple[1].replace(')', '')
						entryAdv = float(entryTuple[1])
						heroAdvMap[entryName.lower()].append(entryAdv)
						if (entryAdv > percentThreshold):
							if (entryName in heroesLeft):
								heroesLeft.remove(entryName)
					pickedHeroes.append(pickedHero)
					pickedHeader = ''
					for hero in pickedHeroes:
						properHero = properFormatName(hero)
						pickedHeader += '{:^20}'.format(properHero)
					print('{:<20}'.format("Hero") + pickedHeader)
					outputHeroesLeft(heroesLeft, heroAdvMap)
				else:
					print("Hero already marked as picked.")
				print("\n\nPicked heroes:")
				for hero in pickedHeroes:
					properHero = properFormatName(hero)
					print(properHero)
		except KeyError:
			print("Invalid hero name '" + pickedHero + "', try again.")
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
	properHero = properHero.replace('Natures', 'Nature\'s')
	return properHero

def prophetFix(heroname):
	if (heroname == '\"Natures Prophet\"'):
		return "Nature\'s Prophet"
	return heroname

def outputHeroesLeft(heroesLeft, heroAdvMap):
	for hero in heroesLeft:
		heroDisplay = '{:<20}'.format(hero)
		advStats = ''
		for adv in heroAdvMap[hero.lower()]:
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
			heroAdvantages = heroAdvMap[hero.lower()]
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
						properHero = properFormatName(hero)
						pickedHeader += '{:<20}'.format(properHero)
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


if __name__ == '__main__':
    main(sys.argv)