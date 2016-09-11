import fileOperators, nameFormater, constantNames, duplicate
from fileOperators import *
from nameFormater import *
from constantNames import *
from duplicate import *

def formShorthands(duplicatesDict, shorthandReset = None):
	if shorthandReset:
		return formDictFromCommaFile(shorthandReset, duplicatesDict)
	return formDictFromCommaFile(SHORTHAND_FILE, duplicatesDict)

def addShorthand(heroname, shorthand, shortLines, shortDict, dupLines, dupDict):
	if shorthand not in shortDict and shorthand not in dupDict:
		for line in shortLines:
			lineSplit = line.split(', ')
			name = lineSplit[0]
			values = lineSplit[1:]
			if ((heroname == name) and (shorthand not in values)):
				newline = line + ", " + shorthand
				shortLines.remove(line)
				shortLines.append(newline)
				break
		updateFile(shortLines, SHORTHAND_FILE)
	else:
		if shorthand in shortDict:
			heroToRemove = shortDict[shorthand]
			shortLines, shortDict, dupLines, dupDict = removeShorthand(shorthand, heroToRemove, shortLines, shortDict, dupLines, dupDict)
			dupLines, dupDict = checkDuplicate(shorthand, heroname, False, dupLines, dupDict)
		dupLines, dupDict = checkDuplicate(shorthand, heroname, False, dupDict, dupLines)
	return shortLines, shortDict, dupLines, dupDict

def removeShorthand(shorthand, heroname, shortLines, shortDict, dupLines, dupDict):
	if shorthand not in shortDict:
		lenDuplicatesPreRemoval = len(dupLines)
		dupLines, dupDict = checkDuplicate(shorthand, heroname, True, dupLines, dupDict)
		if (lenDupLines != lenDupPre):
			shortLines, shortDict, dupLines, dupDict = addShorthand(heroname, shorthand, shortLines, shortDict, dupLines, dupDict)
			updateFile(shortLines, SHORTHAND_FILE)
	else:
		del shortDict[shorthand]
		for line in shortLines:
			splitLine = line.split(', ')
			if (splitLine[0] == heroname):
				shortLines.remove(line)
				newLine = shortLines[0]
				for entry in shortLines[1:]:
					newLine += (', ' + entry)
				dupLines.append(newLine)
		updateFile(shortLines, SHORTHAND_FILE)
	return shortLines, shortDict, dupLines, dupDict

def addShorthands(shortLines, shortDict, dupLines, dupDict, heroAdvMap):
	""" The first search for a key in shortDict is done so that the created shorthands are searched. 
		You can created a shorthand "a" then use that shorthand to add other ones faster."""
	response = 'y'
	while(response == 'y'):
		heroExist = False
		while (not heroExist):
			heroname = input("Enter heroname: ")
			if (heroname in shortDict):
				heroname = shortDict[heroname]
			else:
				heroname = properFormatName(heroname)
			heroExist = heroname in heroAdvMap
			if heroExist is False:
				print("No such hero '" + heroname + "'. Try again.")
		shorthand = input("Enter shorthand (will be forced all lowercase): ").lower()
		if (shorthand not in SHORTHAND_BLACKLIST):
			response = input("Adding shorthand '" + shorthand + "' for hero '" + heroname + "'. Enter 'y' to confirm: ")
			if (response == 'y'):
				shortLines = addShorthand(heroname, shorthand, shortLines, shortDict, dupLines, dupDict)
				shortDict[shorthand] = heroname
				print(shortDict)
				print("Shorthand added.")
			else:
				print("Shorthand cancelled.")
		else:
			print("Sorry, that shorthand is blacklisted. Don't be naughty.")
		response = input("Enter 'y' to continue adding shorthands. Any other input to exit: ")
	return shortLines, shortDict

def resetShorthands(shorthandDict, shorthandLines, duplicateDict, duplicateLines, factoryZero = False):
	if factoryZero:
		shortDict = {}
		shortLines = HEROES_LIST
		updateFile(HEROES_LIST, SHORTHAND_FILE)
	else:
		dupLines, dupDict = formDuplicates(DUPLICATE_RESET_POINT)
		shortLines, shortDict = formShorthands(dupDict, SHORTHAND_RESET_POINT)
	return shortLines, shortDict, dupDict, dupLines