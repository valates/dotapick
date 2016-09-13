import fileOperators, nameFormater, constantNames, pickleSerializers
from fileOperators import *
from nameFormater import *
from constantNames import *
from pickleSerializers import *

""" Creates a dictionary from the file containing all preset hero shorthands
	located in /data/shorthands. Saves the dictionary to a file and returns
	the dictionary. """
def formShorthands():
	shortDict = formDictFromCommaFile(SHORTHAND_FILE)
	save_obj(shortDict, SHORTHAND_PICKLE_NAME)
	return shortDict

""" Associates the string SHORTHAND with the hero with string name HERONAME by adding the
	key, value pair to the dictionary of shorthands, SHORTDICT. Returns the resulting dictionary
	if the key was not already present. Returns SHORTDICT untouched if key SHORTHAND is present. """
def addShorthand(heroname, shorthand, shortDict):
	if shorthand not in shortDict:
		shortDict[shorthand] = heroname
		save_obj(shortDict, SHORTHAND_PICKLE_NAME)
	else:
		print("Shorthand '" + shorthand + "' already present.")
	return shortDict

""" Removes the association between the string SHORTHAND and the hero with string name HERONAME 
	by removing the key from the dictionary, SHORTDICT. Returns the resulting dictionary
	if the key was present. Returns SHORTDICT untouched if key SHORTHAND is not present. """
def removeShorthand(shorthand, heroname, shortDict):
	if shorthand in shortDict:
		print("Shorthand '" + shorthand + "' not present.")
	else:
		del shortDict[shorthand]
		save_obj(shortDict, SHORTHAND_PICKLE_NAME)
	return shortDict

""" Allows the user to add multiple shorthands to the dictionary of shorthand to heroname key, value pairs.
	Checks the hero is present in list HEROLIST of all string names for all heroes. Returns the dictionary 
	SHORTDICT after user has finished associating keys with values contained in HEROLIST. """
def addShorthands(shortDict, heroList):
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
			heroExist = heroname in heroList
			if heroname not in heroList:
				print("No such hero '" + heroname + "'. Try again.")
		shorthand = input("Enter shorthand: ")
		if (shorthand not in SHORTHAND_BLACKLIST):
			response = input("Adding shorthand '" + shorthand + "' for hero '" + heroname + "'. Enter 'y' to confirm: ")
			if (response == 'y'):
				shortDict = addShorthand(heroname, shorthand, shortDict)
				print("Shorthand added.")
			else:
				print("Shorthand cancelled.")
		else:
			print("Sorry, that shorthand is blacklisted. Don't be naughty.")
		response = input("Enter 'y' to continue adding shorthands. Any other input to exit: ")
	return shortDict


""" Creates a new shorthand dictionary and returns it to the caller. If boolean FACTORYZERO
	is True, a blank dictionary is returned. If FACTORYZERO is False, the dictioanry matches
	the contents of /data/shorthands. """
def resetShorthands(factoryZero = False):
	if factoryZero:
		shortDict = {}
		save_obj(shortDict, SHORTHAND_PICKLE_NAME)
	else:
		shortDict = formShorthands()
	return shortDict