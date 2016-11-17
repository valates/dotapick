""" For a file with string name FILENAME, splits the contents based on the
        newline delimiter and returns the split lines as a list. """
def splitFileByNewline(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    return lines

""" For a file with string name FILENAME, collects each line which is of the form 
        'A, B, C, D, ... Z. For all values in the line excluding A (the first string before
        a comma), a key value pair is made where !A is paired with A. The key, value pair
        is added to a dictionary and the dictionary is returned after each line has been parsed
        in this manner. """
def formDictFromCommaFile(filename):
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
                        if curKey not in curDict:
                                curDict[curKey] = listVal
        return curDict
