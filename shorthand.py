from nameFormatter import properFormatName
from pickleSerializers import save_obj
from fileOperators import formDictFromCommaFile
from constantNames import SHORTHAND_FILE, SHORTHAND_PICKLE_NAME

""" Creates a dictionary from the file containing all preset hero shorthands
        located in /data/shorthands. Saves the dictionary to a file. """
def formShorthands():
        shortDict = formDictFromCommaFile(SHORTHAND_FILE)
        save_obj(shortDict, SHORTHAND_PICKLE_NAME)

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
