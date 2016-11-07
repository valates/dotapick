import sys, fileOperators, nameFormater, constantNames, shorthand, pickleSerializers, htmlOperators, time, random, requests
from fileOperators import *
from nameFormater import *
from constantNames import *
from shorthand import *
from pickleSerializers import *
from htmlOperators import htmlSearcher, htmlSearchAll
from random import randint

HEROES_LIST = splitFileByNewline(HERONAME_FILE)

def pullDotabuff():
	heroLen = len(HEROES_LIST)
	heroHtml = splitFileByNewline("data/herohtml")
	heroAdvDict = {}
	dataStart = "<table class=\"sortable\">"
	dataEnd = "</table>"
	advStart = "<td class=\"cell-xlarge\">"
	advCutoff = "<div class=\"bar bar-default\"><div class=\"segment segment-advantage\""
	i = 1
	for hero in HEROES_LIST:
		url = hero.replace(" ","-")
		url = url.lower()
		url = url.replace("'", "")
		url = "http://www.dotabuff.com/heroes/" + url + "/matchups"
		response = requests.get(url, headers = {'User-agent': 'your bot 0.1'})
		while (response.status_code != 200):
			print("Blocked: sleeping for 10-15 minutes")
			time.sleep((10 + randint(0, 5)) * 60)
			response = requests.get(url, headers = {'User Agent': 'your bot 0.1'})
		urlText = response.text
		searchBlock = htmlSearcher(dataStart, dataEnd, urlText, False, True)[0]
		advantages = htmlSearchAll(advStart, advCutoff, searchBlock)
		advBlock = []
		for entry in advantages:
			entryName = entry[:-5]
			entryName = entryName.replace("1", "")
			entryPercent = entry[-5:-1]
			if (entryName[-1] == '-'):
				entryName = entryName[:-1]
				entryPercent = '-' + entryPercent
			entryTuple = (entryName, entryPercent)
			advBlock.append(entryTuple)
		heroAdvDict[hero] = advBlock
		print('{:<20}'.format(hero) + "\t" + str(i) + "/" + str(heroLen))
		i += 1
	save_obj(heroAdvDict, ADV_PICKLE_NAME)
	formShorthands()