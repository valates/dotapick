import argparse
import sys
from fileOperators import *
from nameFormater import *
from constantNames import *
from shorthand import *
from pickleSerializers import *
from htmlOperators import htmlSearcher, htmlSearchAll
from heroFileFormatter import pullDotabuff
from pythonShortcomings import iterateAndRemove

#TODO help option output from file contents

def main(args):
	argc = len(sys.argv)
	argv = sys.argv
	if (argc == 2):
		if (argv[1].lower() == "--pulldotabuff"):
			pullDotabuff()
		if (argv[1].lower() == "--reset"):
			save_obj(2.0, THRESHOLD_PICKLE_NAME)
			save_obj("", SORTING_PICKLE_NAME)
			resetShorthands()
		if (argv[1].lower() == "--setsort"):
			save_obj("", SORTING_PICKLE_NAME)
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
	heroAdvantageDict = load_obj(ADV_PICKLE_NAME)
	shortDict = load_obj(SHORTHAND_PICKLE_NAME)
	pickedHeroes = []
	heroAdvMap, heroesLeft = initHeroAdvs()

	informationPool[] = {}
	informationPool["percentThreshold"] = load_obj(THRESHOLD_PICKLE_NAME)
	informationPool["sortPrefix"] = load_obj(SORTING_PICKLE_NAME)
	informationPool["heroAdvantageDict"] = load_obj(ADV_PICKLE_NAME)
	informationPool["shortDict"] = load_obj(SHORTHAND_PICKLE_NAME)
	informationPool["pickedHeroes"] = []
	informationPool["heroAdvMap"] = heroAdvMap
	informationPool["heroesLeft"] = heroesLeft
	performSort(heroesLeft, heroAdvMap, pickedHeroes, sortPrefix)
	while (len(pickedHeroes) < 5):
		print("\n")
		commands = input("Enter picked hero, 'sort,' to sort current, or 'q' to quit: ").lower()
		commands = commands.split(",")
		for pickedHero in commands:
			pickedHero = pickedHero.strip()
			if (len(pickedHeroes) == 5):
				break
			elif (pickedHero == KILL_COMMAND):
				exit()
			elif(pickedHero == ""):
				performSort(heroesLeft, heroAdvMap, pickedHeroes, sortOption)
			elif (pickedHero in SORT_INPUTS):
				print("Not currently in sorting function. Enter 'sort' with a sort command to sort current data.")
			elif (pickedHero[:4] == "undo"):
				undoCommand = pickedHero.split(" ")
				if (len(undoCommand) == 1):
					properHero = pickedHeroes[-1]
				else:
					properHero, shortDict = findHero(pickedHero[5:], shortDict, pickedHeroes)
				if (properHero is not None):
					pickedHeroes, heroesLeft, heroAdvMap = undoPick(properHero, pickedHeroes, heroesLeft, heroAdvantageDict, heroAdvMap, percentThreshold, sortPrefix)
				else:
					print(properHero + " not present in picked heroes. Try again.")
			elif (pickedHero[:6] == "repick"):
				repickedCommand = pickedHero.split(" ")
				if (len(repickedCommand) != 3):
					print("Insufficient arguments to repick command.")
				else:
					properRemoveHero, shortDict = findHero(repickedCommand[1], shortDict, pickedHeroes)
					properPickHero, shortDict = findHero(repickedCommand[2], shortDict, [hero for hero in HEROES_LIST if hero not in pickedHeroes])
					if (properRemoveHero is not None):
						if (properPickHero is not None):
							pickedHeroes, heroesLeft, heroAdvMap = undoPick(properRemoveHero, pickedHeroes, heroesLeft, heroAdvantageDict, heroAdvMap, percentThreshold, sortPrefix)
							pickedHeroes, heroesLeft, heroAdvMap, shortDict = pickHero(properPickHero, shortDict, pickedHeroes, heroesLeft, heroAdvantageDict, heroAdvMap, percentThreshold, sortPrefix)
						else:
							print("Invalid hero to pick in place of hero you are removing.")
					else:
						print("Invalid hero to remove.")
			elif (pickedHero[:4] == "find"):
				properHero, shortDict = findHero(pickedHero[4:].strip(), shortDict, HEROES_LIST)
				if (properHero is not None):
					if (properHero in heroesLeft):
						print("Finding " + properHero)
						performSort([properHero], heroAdvMap, pickedHeroes, sortPrefix)
					else:
						print("Hero not left in remaining hero pool. Ill advised to pick.")
				else:
					print("Invalid hero to search.")
			elif (pickedHero[:4] == "sort"):
				sortTokens = pickedHero.split(' ')
				if (len(sortTokens) == 1):
					print("Enter a sorting command (sum, average, 1-5) as well.")
				else:
					performSort(heroesLeft, heroAdvMap, pickedHeroes, sortTokens[1])
			elif (pickedHero[:5] == "focus"):
				focusTokens = pickedHero.split(" ")
				if ((len(focusTokens) > 1) and (focusTokens[1] in ROLES_NAMES)):
					heroesLeft = focusRemainingHeroPool(focusTokens[1], heroesLeft, heroAdvMap, pickedHeroes, sortPrefix)
			elif (pickedHero[:5] == "prune"):
				heroesLeft = pruneHeroesByRole(pickedHero, heroesLeft, heroAdvMap, pickedHeroes, sortPrefix)
			elif ((pickedHero[:3].lower() == BAN_COMMAND) and (pickedHero[3].lower() != 'e')):
				heroesLeft = banHero(pickedHero, shortDict, heroesLeft, heroAdvMap, pickedHeroes, sortPrefix)
			else:
				pickedHeroes, heroesLeft, heroAdvMap, shortDict= pickHero(pickedHero, shortDict, pickedHeroes, heroesLeft, heroAdvantageDict, heroAdvMap, percentThreshold, sortPrefix)
	while (True):
		print("Enter " + KILL_COMMAND + " at any time to quit sorting.")
		sortOption = input("\n\nEnter sorting method (" + SORT_INPUTS[0] + ", " + SORT_INPUTS[1] + ", or 1-5): ").lower()
		if (sortOption == KILL_COMMAND):
			break
		performSort(heroesLeft, heroAdvMap, pickedHeroes, sortOption)

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
	return shortDict, heroToReturn

def undoPick(properHero, pickedHeroes, heroesLeft, heroAdvantageDict, heroAdvMap, percentThreshold, sortPrefix):
	pickedHeroes.remove(properHero)
	heroAdvMap, heroesLeft = initHeroAdvs()
	pickedCopy = []
	for hero in pickedHeroes:
		pickedCopy, heroesLeft, heroAdvMap = performAdvantageSearch(hero, pickedCopy, heroesLeft, heroAdvantageDict, heroAdvMap, percentThreshold, sortPrefix)
	return pickedCopy, heroesLeft, heroAdvMap

def initHeroAdvs():
	heroAdvMap, heroesLeft = {}, []
	for hero in HEROES_LIST:
		heroAdvMap[hero] = []
		heroesLeft.append(hero)
	return heroAdvMap, heroesLeft

def findHero(pickedHero, shortDict, heroesToCheckForPick):
	if (pickedHero in shortDict):
		properHero = shortDict[pickedHero]
	else:
		properHero = properFormatName(pickedHero)
	if (properHero not in HEROES_LIST):
		shortDict, properHero = addToShorthands(pickedHero, shortDict)
	if (properHero not in heroesToCheckForPick):
		return None, shortDict
	return properHero, shortDict

def focusRemainingHeroPool(focusSpecifier, heroesLeft, heroAdvMap, pickedHeroes, sortPrefix):
	toFocus = splitFileByNewline("data/" + focusSpecifier)
	heroesLeft = iterateAndRemove(heroesLeft, lambda toFocus, entry: entry not in toFocus, toFocus)
	performSort(heroesLeft, heroAdvMap, pickedHeroes, sortPrefix)
	return heroesLeft

def pickHero(pickedHero, shortDict, pickedHeroes, heroesLeft, heroAdvantageDict, heroAdvMap, percentThreshold, sortPrefix):
	properHero, shortDict = findHero(pickedHero, shortDict, HEROES_LIST)
	if (properHero is not None):
		pickedHeroes, heroesLeft, heroAdvMap = performAdvantageSearch(properHero, pickedHeroes, heroesLeft, heroAdvantageDict, heroAdvMap, percentThreshold, sortPrefix)
	return pickedHeroes, heroesLeft, heroAdvMap, shortDict

def pruneHeroesByRole(pickedHero, heroesLeft, heroAdvMap, pickedHeroes, sortPrefix): #TODO turn into call for other cousin of this
#TODO MAKE SURE WORKING
	pruneTokens = pickedHero.split(" ")
	if (pruneTokens[1] in ROLES_NAMES):
		toPrune = splitFileByNewline("data/" + pruneTokens[1])
		remainingRoles = []
		for role in ROLES_NAMES:
			if (role != pruneTokens[1]):
				currentRoleList = splitFileByNewline("data/" + role)
				remainingRoles.append(currentRoleList)
		for hero in toPrune:
			noOverlap = True
			for heroList in remainingRoles:
				if (hero in heroList):
					noOverlap = False
			if (noOverlap):
				heroesLeft.remove(hero)
		performSort(heroesLeft, heroAdvMap, pickedHeroes, sortPrefix)
	return heroesLeft

def banHero(pickedHero, shortDict, heroesLeft, heroAdvMap, pickedHeroes, sortPrefix):
	properHero, shortDict = findHero(pickedHero[3:].strip(), shortDict, heroesLeft)
	if (pickedHero is not None):
		heroesLeft.remove(pickedHero)
		print(pickedHero + " banned.")
		performSort(heroesLeft, heroAdvMap, pickedHeroes, sortPrefix)
	else:
		print("'" + pickedHero + "' not present in hero list. Try again.")
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

def performSort(heroesLeft, heroAdvMap, pickedHeroes, sortOption):
	if (sortOption == "" or len(pickedHeroes) == 0):
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
				heroDisplay = '{:<20}'.format(sumEntry[0]) + '\t\t' + '{0:.2f}'.format(sumEntry[1])
				print(heroDisplay)
		else:
			if (sortOption in SORT_INPUTS[2:]):
				sortOption = int(sortOption)
				if (sortOption <= len(pickedHeroes)):
					sortValues = sorted(sortValues, key=lambda curList: (curList[1])[(sortOption - 1)], reverse=True)
					pickedHeader = ''
					for hero in pickedHeroes:
						pickedHeader += '{:>20}'.format(hero)
					print('{:<20}'.format("Hero") + pickedHeader)
					for sortEntry in sortValues:
						heroDisplay = '{:<20}'.format(sortEntry[0])
						advStats = ''
						for adv in sortEntry[1]:
							advStats += '{:>20}'.format(adv)
						print(heroDisplay + advStats)
				else:
					print("Insufficient number of picked heroes to sort by column '" + str(sortOption) + "'")
			else:
				print("Invalid sorting column '" + sortOption + "'")

if __name__ == '__main__':
    main(sys.argv)