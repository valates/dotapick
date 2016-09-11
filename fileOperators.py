import os, constantNames
from constantNames import TEMP_NAME
from os import remove, rename

def splitFileByNewline(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    return lines

def updateFile(lines, filename):
	tmpFile = open(TEMP_NAME, 'w')
	for line in lines:
		tmpFile.write((line + '\n'))
	tmpFile.close()
	os.remove(filename)
	os.rename(TEMP_NAME, filename)

def resetFile(savedFactory, filename):
	savedContents = splitFileByNewline(savedFactory)
	updateFile(savedContents, filename)

def formDictFromCommaFile(filename, duplicates = {}):
	lines = splitFileByNewline(filename)
	commaLists = []
	for line in lines:
		lineList = line.split(', ')
		if (len(lineList) != 1):
			commaLists.append(lineList)
	curDict = {}
	for entry in commaLists:
		listKeys = entry[1:]
		listVal = entry[0]
		for curKey in listKeys:
			if curKey not in duplicates:
				curDict[curKey] = listVal
	return lines, curDict