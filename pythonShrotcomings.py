def iterateAndRemove(inputList, conditionOfRemoval):
	outputList = [val for val in inputList]
	for entry in inputList:
		if (conditionOfRemoval(entry)):
			outputList.remove(entry)
	return outputList

