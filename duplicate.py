import fileOperators, constantNames, shorthand
from fileOperators import *
from constantNames import DUPLICATE_FILE
from shorthand import *

def formDuplicates(duplicateReset = None):
	if duplicateReset:
		return formDictFromCommaFile(duplicateReset)
	return formDictFromCommaFile(DUPLICATE_FILE)

def checkDuplicate(shorthand, heroname, removing, dupLines, dupDict):
	shorthandPresent = shorthand in dupDict
	if (removing):
		if ((shorthandPresent) and (heroname in dupDict[shorthand])):
			dupDict[shorthand] = [hero for hero in dupDict[shorthand] if hero != heroname]
			if (len(dupDict[shorthand]) == 0):
				del dupDict[shortHand]
			for line in dupLines:
				lineTokens = line.split(', ')
				if (lineTokens[0] == shorthand):
					dupLines.remove(line)
					if (len(lineTokens) != 2):
						newLine = lineTokens[0]
						for entry in lineToken[1:]:
							newLine += (', ' + entry)
						dupLines.append(newLine)
					break
	else:
		if shorthandPresent:
			dupDict[shorthand] = heroname
			for line in dupLines:
				if ((line.split(', '))[0] == shorthand):
					dupLines.remove(line)
					dupLines.append((line + ', ' + heroname))
					break
		else:
			dupDict[shortHand] = dupDict[shorthand] + [heroname]
			newLine = shorthand + ', ' + heroname
			dupLines.append(newLine)
	updateFile(dupLines, DUPLICATE_FILE)
	return dupLines, dupDict