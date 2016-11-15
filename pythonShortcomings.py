def iterateAndRemove(inputList, conditionOfRemoval, toAct):
	outputList = [val for val in inputList]
	for entry in inputList:
		if (conditionOfRemoval(toAct, entry)):
			outputList.remove(entry)
	return outputList