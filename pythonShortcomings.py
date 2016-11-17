""" Takes the list, INPUTLIST, and remvoes all entries in said list
	based on the input function CONDITIONOFREMOVAL. If multiple specific
	entries are to be removed, they are specific in the optional input list
	TOACT. If TOACT is None, the input function should account for this factor. 
	Input function CONDITIONOFREMOVAL takes two paramaters: the optional list
	of specific entries to remove, TOACT, and the current list entry to check, ENTRY. """
def iterateAndRemove(inputList, conditionOfRemoval, toAct = None):
	outputList = [val for val in inputList]
	for entry in inputList:
		if (conditionOfRemoval(toAct, entry)):
			outputList.remove(entry)
	return outputList