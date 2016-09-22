import sys, fileOperators, nameFormater, constantNames, shorthand, pickleSerializers, htmlOperators
from fileOperators import *
from nameFormater import *
from constantNames import *
from shorthand import *
from pickleSerializers import *
from htmlOperators import htmlSearcher, htmlSearchAll

def formatAdv():
	heroLen = len(HEROES_LIST)
	heroHtml = splitFileByNewline("data/herohtml")
	heroAdvDict = {}
	dataStart = "<table class=\"sortable\">"
	dataEnd = "</table>"
	advStart = "<td class=\"cell-xlarge\">"
	advCutoff = "<div class=\"bar bar-default\"><div class=\"segment segment-advantage\""
	for hero in HEROES_LIST:
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
			heroAdvDict[hero] = advBlock
		print('{:<20}'.format(hero) + "\t" + str(heroLen - len(heroHtml)) + "/" + str(heroLen))
	save_obj(heroAdvDict, ADV_PICKLE_NAME)
	formShorthands()