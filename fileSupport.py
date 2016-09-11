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