from constantNames import SORT_INPUTS

""" Sorts the heroes not prunes stored in the list HEROESLEFT. Uses the contents
        dictionary HEROADVMAP which contains the % advantage each hero in list PICKEDHEROES
        has against the hero in HEROESLEFT. Sorts based on the string specifier SORTOPTION. """
def performSort(heroesLeft, heroAdvMap, pickedHeroes, sortOption):
        if (sortOption == "" or len(pickedHeroes) == 0):
                pickedHeader = ''
                for hero in pickedHeroes:
                        pickedHeader += '{:<20}'.format(hero)
                print('{:<20}'.format("Hero") + pickedHeader)
                for hero in heroesLeft:
                        heroDisplay = '{:<20}'.format(hero)
                        advStats = ''
                        for adv in heroAdvMap[hero]:
                                advStats += '{:^20}'.format(adv) + "\t"
                        print(heroDisplay + "\t" + advStats)
                print(str(len(heroesLeft)) + " heroes remaining.")
        else:
                sortValues = []
                for hero in heroesLeft:
                        heroAdvantages = heroAdvMap[hero]
                        heroTuple = (hero, heroAdvantages)
                        sortValues.append(heroTuple)
                if (sortOption in SORT_INPUTS[:2]):
                        sumList = []
                        for entry in sortValues:
                                entryName = entry[0]
                                entryList = entry[1]
                                entrySum = 0
                                for value in entryList:
                                        entrySum += value
                                if (sortOption == SORT_INPUTS[1]):
                                        entrySum /= len(pickedHeroes)
                                sumTuple = (entryName, entrySum)
                                sumList.append(sumTuple)
                        sumList = sorted(sumList, key=lambda curSum: curSum[1], reverse=True)
                        for sumEntry in sumList:
                                heroDisplay = '{:<20}'.format(sumEntry[0]) + '\t\t' + '{0:.2f}'.format(sumEntry[1])
                                print(heroDisplay)
                else:
                        if (sortOption in SORT_INPUTS[2:]):
                                sortOption = int(sortOption)
                                if (sortOption <= len(pickedHeroes)):
                                        sortValues = sorted(sortValues, key=lambda curList: (curList[1])[(sortOption - 1)], reverse=True)
                                        pickedHeader = ''
                                        for hero in pickedHeroes:
                                                pickedHeader += '{:>20}'.format(hero)
                                        print('{:<20}'.format("Hero") + pickedHeader)
                                        for sortEntry in sortValues:
                                                heroDisplay = '{:<20}'.format(sortEntry[0])
                                                advStats = ''
                                                for adv in sortEntry[1]:
                                                        advStats += '{:>20}'.format(adv)
                                                print(heroDisplay + advStats)
                                else:
                                        print("Insufficient number of picked heroes to sort by column '" + str(sortOption) + "'")
                        else:
                                print("Invalid sorting column '" + sortOption + "'")
