import sys, fileOperators, nameFormater, constantNames, shorthand, pickleSerializers, htmlOperators, heroFileFormatter
from fileOperators import *
from nameFormater import *
from constantNames import *
from shorthand import *
from pickleSerializers import *
from htmlOperators import htmlSearcher, htmlSearchAll
from heroFileFormatter import pullDotabuff

#TODO help option output from file contents
#TODO comment functions

#Make so presetting a sort value behaves as it should for sum, average- right now preserves column names

HEROES_LIST = splitFileByNewline(HERONAME_FILE)

def main(args):
	argc = len(sys.argv)
	argv = sys.argv
	if (argc == 2):
		if (argv[1].lower() == "--pulldotabuff"):
			pullDotabuff()
		if (argv[1].lower() == "--reset"):
			save_obj(2.0, THRESHOLD_PICKLE_NAME)
			save_obj(None, SORTING_PICKLE_NAME)
			resetShorthands()
		if (argv[1].lower() == "--setsort"):
			save_obj(None, SORTING_PICKLE_NAME)
	elif ((argc == 4) and (argv[1].lower() == "--addshort")):
		addShorthand(properFormatName(argv[2]), argv[3], shortDict)
	else:
		if (argc == 3):
			if (argv[1].lower() == "--setpercent"):
				try:
					percentThreshold = float(argv[2])
					save_obj(percentThreshold, THRESHOLD_PICKLE_NAME)
				except ValueError:
					print("Invalid float value, '" + argv[2] + ",' inputted. Continuing with previous value.")
			if (argv[1].lower() == "--setsort"):
				if (argv[2].lower() in SORT_INPUTS):
					save_obj(argv[2].lower(), SORTING_PICKLE_NAME)
				else:
					print("Invalid sorting value, '" + argv[2] + "'. Continuing with previous value.")
		startPicks()


def startPicks():
	percentThreshold = load_obj(THRESHOLD_PICKLE_NAME)
	sortPrefix = load_obj(SORTING_PICKLE_NAME)
	print(sortPrefix)
	if (sortPrefix == "None"):
		sortPrefix = None
	heroAdvantageDict = load_obj(ADV_PICKLE_NAME)
	shortDict = load_obj(SHORTHAND_PICKLE_NAME)
	heroAdvMap = {}
	heroesLeft = []
	pickedHeroes = []
	for hero in HEROES_LIST:
		heroAdvMap[hero] = []
		heroesLeft.append(hero)
	performSort(heroesLeft, heroAdvMap, pickedHeroes, sortPrefix)
	while (len(pickedHeroes) < 5):
		print("\n")
		pickedHero = input("Enter picked hero, 'sort,' to sort current, or 'q' to quit: ").lower()
		if (pickedHero == KILL_COMMAND):
			exit()
		elif (pickedHero in SORT_INPUTS):
			print("Not currently in sorting function. Entry 'sort' to switch.")
		elif(pickedHero[:7]=="setsort"):
			sortToSet = (pickedHero.split(" "))[1]
			if (sortToSet in SORT_INPUTS):
				sortPrefix = sortToSet
			elif(sortToSet == "None"):
				sortPrefix = None
			else:
				print("Please enter a valid sorting command.")
			performSort(heroesLeft, heroAdvMap, pickedHeroes, sortPrefix)
		elif (pickedHero[:4] == "undo"):
			undoCommand = pickedHero.split(" ")
			if (len(undoCommand) == 1):
				properHero = pickedHeroes[-1]
			else:
				pickedHero = pickedHero[5:]
				if (pickedHero in shortDict):
					properHero = shortDict[pickedHero]
				else:
					properHero = properFormatName(pickedHero)
			if (properHero in pickedHeroes):
				pickedHeroes.remove(properHero)
				heroesLeft = []
				for hero in HEROES_LIST:
					heroAdvMap[hero] = []
					heroesLeft.append(hero)
				pickedCopy = []
				for hero in pickedHeroes:
					hero, pickedCopy, heroesLeft, heroAdvantageDict, heroAdvMap = performAdvantageSearch(hero, 
																										 pickedCopy, 
																										 heroesLeft, 
																										 heroAdvantageDict, 
																										 heroAdvMap, 
																										 percentThreshold,
																										 sortPrefix)
				pickedHeroes = pickedCopy
			else:
				print(properHero + " not present in picked heroes. Try again.")
		elif (pickedHero[:6] == "repick"):
			repickedCommand = pickedHero.split(" ")
			if (len(repickedCommand) != 3):
				print("Insufficient arguments to repick command.")
			else:
				removingHero = repickedCommand[1] 
				pickingHero = repickedCommand[2]

				if (removingHero in shortDict):
					properRemoveHero = shortDict[removingHero]
				else:
					properRemoveHero = properFormatName(removingHero)

				if (pickingHero in shortDict):
					properPickHero = shortDict[pickingHero]
				else:
					properPickHero = properFormatName(pickingHero)
			if (properRemoveHero in pickedHeroes):
				if (properPickHero in pickedHeroes):
					print(properPickHero + " already picked. Repick with a different hero.")
				else: 
					pickedHeroes.remove(properRemoveHero)
					heroesLeft = []
					for hero in HEROES_LIST:
						heroAdvMap[hero] = []
						heroesLeft.append(hero)
					pickedCopy = []
					for hero in pickedHeroes:
						hero, pickedCopy, heroesLeft, heroAdvantageDict, heroAdvMap = performAdvantageSearch(hero, 
																											 pickedCopy, 
																											 heroesLeft, 
																											 heroAdvantageDict, 
																											 heroAdvMap, 
																											 percentThreshold,
																											 sortPrefix)
					pickedHeroes = pickedCopy
					properPickHero, pickedHeroes, heroesLeft, heroAdvantageDict, heroAdvMap = performAdvantageSearch(properPickHero, 
																										 		     pickedHeroes, 
																												     heroesLeft, 
																												     heroAdvantageDict, 
																												     heroAdvMap, 
																												     percentThreshold,
																											         sortPrefix)
			else:
				print(properRemoveHero + " not present in picked heroes. Try again.")
		elif (pickedHero[:4] == "sort"):
			if (len(pickedHeroes) == 0):
				print("Cannot sort without any advantages. Pick a hero first.")
			else:
				print((pickedHero.split(' '))[1])
				performSort(heroesLeft, heroAdvMap, pickedHeroes, (pickedHero.split(' '))[1])
		elif(pickedHero[:5] == "prune"):
			pruneTokens = pickedHero.split(" ")
			if (pruneTokens[1] in ROLES_NAMES):
				toPrune = splitFileByNewline("data/" + pruneTokens[1])
				remainderFiles = [x for x in ROLES_NAMES if (x != pruneTokens[1])]
				if ((len(pruneTokens) == 3) and (pruneTokens[2] == "--harsh")):
					remainder1, remainder2 = [], []
				else:
					remainder1 = splitFileByNewline("data/" + remainderFiles[0])
					remainder2 = splitFileByNewline("data/" + remainderFiles[1])
				for hero in toPrune:
					if ((hero in heroesLeft) and (hero not in remainder1) and (hero not in remainder2)):
						heroesLeft.remove(hero)
				performSort(heroesLeft, heroAdvMap, pickedHeroes, sortPrefix)
		elif((pickedHero[:3].lower() == BAN_COMMAND) and (pickedHero[:4].lower() != 'bane')):
			pickedHero = pickedHero[3:].strip()
			print(pickedHero)
			if (pickedHero in shortDict):
				pickedHero = shortDict[pickedHero]
			else:
				pickedHero = properFormatName(pickedHero)
			if (pickedHero in heroesLeft):
				heroesLeft.remove(pickedHero)
				print(pickedHero + " banned.")
				performSort(heroesLeft, heroAdvMap, pickedHeroes, sortPrefix)
			else:
				print("'" + pickedHero + "' not present in hero list. Try again.")
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
																											percentThreshold,
																											sortPrefix)
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
						properHero, pickedHeroes, heroesLeft, heroAdvantageDict, heroAdvMap = performAdvantageSearch(heroToMap, 
																													pickedHeroes, 
																													heroesLeft, 
																													heroAdvantageDict, 
																													heroAdvMap, 
																													percentThreshold,
																													sortPrefix)
				else:
					print("Invalid hero name '" + heroToMap + "', not adding to shorthands. Please enter a real name.")
	while(True):
		print("Enter " + KILL_COMMAND + " at any time to quit sorting.")
		sortOption = input("\n\nEnter sorting method (" + SORT_INPUTS[0] + ", " + SORT_INPUTS[1] + ", or 1-5): ").lower()
		if (sortOption == KILL_COMMAND):
			break
		performSort(heroesLeft, heroAdvMap, pickedHeroes, sortOption)

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
	return properHero, pickedHeroes, heroesLeft, heroAdvantageDict, heroAdvMap

def performSort(heroesLeft, heroAdvMap, pickedHeroes, sortOption):
	if (sortOption is None or len(pickedHeroes) == 0):
		pickedHeader = ''
		for hero in pickedHeroes:
			pickedHeader += '{:<20}'.format(hero)
		print('{:<20}'.format("Hero") + pickedHeader)
		for hero in heroesLeft:
			heroDisplay = '{:<20}'.format(hero)
			advStats = ''
			for adv in heroAdvMap[hero]:
				advStats += '{:^20}'.format(adv) + "\t"
			print(heroDisplay + "\t" + advStats)
		print(str(len(heroesLeft)) + " heroes remaining.")
	else:
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
			sumList = sorted(sumList, key=lambda curSum: curSum[1], reverse=True)
			for sumEntry in sumList:
				heroDisplay = '{:<20}'.format(sumEntry[0]) + '\t' + '{0:.2f}'.format(sumEntry[1])
				print(heroDisplay)
		else:
			if (sortOption in SORT_INPUTS[2:]):
				sortOption = int(sortOption)
				if (sortOption <= len(pickedHeroes)):
					sortValues = sorted(sortValues, key=lambda curList: (curList[1])[(sortOption - 1)], reverse=True)
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