import requests
import fake_useragent
import json
import re
import sys
import time
import random
from requests.exceptions import MissingSchema


def splitFileByNewline(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    return lines

HEROES_LIST = splitFileByNewline("heroes.txt")

def main(args):
    argc = len(sys.argv)
    argv = sys.argv[1:]
    percentThrehold = 0.5
    if (argc == 3):
    	percentThrehold = float(argv[1])
    if (argv[0] == "pull"):
    	pullDotabuff()
    elif (argv[0] == "pick"):
    	startPicks(percentThrehold )
    else:
    	exit()

def pullDotabuff():
	print("Dotabuff pull initiated")
	heroCount = 0
	heroLen = len(HEROES_LIST)
	heroHtml = splitFileByNewline("herohtml.txt")

	dataStart = "<table class=\"sortable\">"
	dataEnd = "</table>"
	advStart = "<td class=\"cell-xlarge\">"
	advCutoff = "<div class=\"bar bar-default\"><div class=\"segment segment-advantage\""
	urlPre = "http://www.dotabuff.com/heroes/"
	urlPost = "/matchups"
	heroData = open("heromatch.txt", "a")
	for hero in HEROES_LIST:
		heroUrl = urlPre + (hero.lower()).replace(" ", "-") + urlPost
		#urlOut = requests.get(heroUrl)
		#print(urlOut.text)
		#while (urlOut.status_code == 429):
	#		print("Blocked- sleeping")
	#		time.sleep(60*60 + 30*random.random())
	#		urlOut = requests.get(heroUrl)

		urlText = heroHtml.pop(0)
		if (urlText):
			searchBlock = htmlSearcher(dataStart, dataEnd, urlText, False, True)[0]
			advantages = htmlSearchAll(advStart, advCutoff, searchBlock)
			advBlock = []
			for entry in advantages:
				entryName = entry[:-5]
				entryPercent = entry[-5:-1]
				if (entryName[-1] == '-'):
					entryName = entryName[:-1]
					entryPercent = '-' + entryPercent
				entryTuple = (entryName, entryPercent)
				advBlock.append(entryTuple)
			heroData.write(str(advBlock) + "\n")

		heroCount += 1
		print(hero + "\t" + str(heroCount) + "/" + str(heroLen))

	heroData.close()

def startPicks(percentThrehold ):
	matchupData = splitFileByNewline("heromatch.txt")
	heroDict = {}
	heroAdvMap = {}
	heroCount = 0
	heroesLeft = []
	for hero in HEROES_LIST:
		heroDict[hero.lower()] = heroCount
		heroAdvMap[hero.lower()] = []
		heroesLeft.append(hero)
		heroCount += 1
	pickedHeroes = []
	for hero in heroesLeft:
		heroDisplay = '{:<20}'.format(hero)
		advStats = ''
		for adv in heroAdvMap[hero.lower()]:
			advStats += '{:<20}'.format(adv) + "\t"
		print(heroDisplay + "\t" + advStats)
	print(str(len(heroesLeft)) + " heroes remaining.")
	while (len(pickedHeroes) < 5):
		print("\n")
		pickedHero = input("Enter picked hero: ").lower()
		print("\n**********\n")
		if (pickedHero not in pickedHeroes):
			properHero = ''
			for i in range(0, len(pickedHero)):
				if ((i == 0) or (pickedHero[(i - 1)] == ' ')):
					properHero += pickedHero[i].capitalize()
				else:
					properHero += pickedHero[i]
			if properHero in heroesLeft:
				heroesLeft.remove(properHero)
			heroAdvs = matchupData[heroDict[pickedHero]]
			heroAdvs = heroAdvs[1:-1]
			heroAdvs = heroAdvs.split('), ')
			for entry in heroAdvs:
				entry = entry[1:]
				entry = entry.replace('\'', '')
				entryTuple = entry.split(', ')
				entryName = entryTuple[0]
				entryTuple[1] = entryTuple[1].replace(')', '')
				entryAdv = float(entryTuple[1])
				if (entryName == '\"Natures Prophet\"'):
					heroAdvMap["Nature\'s Prophet".lower()].append(entryAdv)
				else:
					heroAdvMap[entryName.lower()].append(entryAdv)
				if (entryAdv > percentThrehold):
					if (entryName in heroesLeft):
						heroesLeft.remove(entryName)
			pickedHeroes.append(pickedHero)
			pickedHeader = ''
			for hero in pickedHeroes:
				properHero = ''
				for i in range(0, len(hero)):
					if ((i == 0) or (hero[(i - 1)] == ' ')):
						properHero += hero[i].capitalize()
					else:
						properHero += hero[i]
				pickedHeader += '{:<20}'.format(properHero)
			print('{:<20}'.format('') + pickedHeader)
			for hero in heroesLeft:
				heroDisplay = '{:<20}'.format(hero)
				advStats = ''
				for adv in heroAdvMap[hero.lower()]:
					advStats += '{:<20}'.format(adv) + "\t"
				print(heroDisplay + "\t" + advStats)
			print(str(len(heroesLeft)) + " heroes remaining.")
		else:
			print("Hero already marked as picked.")
		print("\n\nPicked heroes:")
		for hero in pickedHeroes:
			properHero = ''
			for i in range(0, len(hero)):
				if ((i == 0) or (hero[(i - 1)] == ' ')):
					properHero += hero[i].capitalize()
				else:
					properHero += hero[i]
			print(properHero)

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

if __name__ == '__main__':
    main(sys.argv)