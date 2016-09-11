def htmlSearcher(startText, stopText, line, giveNull = False, haltBracketKilling = False, startAtStart = False):
	startIndex = line.find(startText)
	startLen = len(startText)
	if startAtStart:
		line = line[startIndex:]
	stopIndex = line.find(stopText)
	hold = 0
	if (stopIndex < startIndex): 
		line = line[startIndex + len(startText):]
		hold = startIndex
		startLen = 0
		startIndex = 0
		stopIndex = line.find(stopText)
	if ((startIndex != -1) and (stopIndex != -1)):
		if haltBracketKilling:
			return (removeCommonArtifacts(line[startIndex + startLen:stopIndex]), stopIndex + hold)
		return (removeCommonArtifacts(removeBrackets(line[startIndex + startLen:stopIndex])), stopIndex + hold)
	if (giveNull):
		return ("null", -1)
	return None
	
def htmlSearchAll(startText, stopText, line, haltBracketKilling = False, startAtStart = False):
	lastStop = 0
	tokenTuple = htmlSearcher(startText, stopText, line, True, haltBracketKilling)
	tokens = []
	while (tokenTuple[1] != -1):
		lastStop = tokenTuple[1]
		tokens.append(tokenTuple[0])
		line = line[lastStop:]
		tokenTuple = htmlSearcher(startText, stopText, line, True, haltBracketKilling, False)
	
	return tokens
	
	
def removeBrackets(text):
	lenText = len(text)
	inBrackets = False
	finalText = ""
	for i in range(lenText):
		curChar = text[i]
		if (curChar == '<'):
			inBrackets = True
		else:
			if (inBrackets is False):
				finalText += curChar
			if (curChar == '>'):
				inBrackets = False
	return finalText
	
def removeCommonArtifacts(text): 
    text = text.replace("&nbsp;", "")
    text = text.replace("&quot;", "\"")
    text = text.replace("&#039;", "'")
    text = text.replace("&#39;", "'")
    text = text.replace("&#8217;", "'")
    text = text.replace("&#8220;", "\"")
    text = text.replace("&#8221;", "\"")
    text = text.replace("&amp;", "&")
    text = text.replace("\\", "")
    text = text.replace("<br>ot", " ")
    return text