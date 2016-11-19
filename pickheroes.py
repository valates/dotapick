import argparse
from constantNames import THRESHOLD_PICKLE_NAME, SORTING_PICKLE_NAME, SORTING_PICKLE_NAME, ADV_PICKLE_NAME, SHORTHAND_PICKLE_NAME, KILL_COMMAND, ROLES_NAMES, SORT_INPUTS, HEROES_LIST, BAN_COMMAND
from pickleSerializers import save_obj, load_obj
from heroFileFormatter import pullDotabuff
from sorting import performSort
from shorthand import resetShorthands
from heroes import initHeroAdvs, findHero, pickHero, banHero,  undoPick, focusRemainingHeroPool


#TODO change setsort to include some value to signift sort by alphabet

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dotabuff", 
                    help="Pulls hero data from dotabuff",
                    action="store_true")
parser.add_argument("-r", "--reset",         
                    help="Sets the percent threshold back to 2.0, resets sorting setting to default to alphabet sorting, and removes all user created shorthands.",
                    action="store_true")
parser.add_argument("-s", "--sort", type=str,
                    help="Changes the default sorting option to one specified. Sorts by alphabet if no input argument.")
parser.add_argument("-p", "--percent", type=float,
                    help="Changes the percent threshold above which opposing heroes are pruned. For each picked hero, any hero the picked hero has a percent advantage > our percent threshold is pruned.")

args = parser.parse_args()
if args.dotabuff:
    pullDotabuff()
if args.reset:
    save_obj(2.0, THRESHOLD_PICKLE_NAME)
    save_obj("", SORTING_PICKLE_NAME)
    resetShorthands()
if args.sort:
    if (args.sort in SORT_INPUTS):
        save_obj(args.sort, SORTING_PICKLE_NAME)
    else:
        print("Invalid sorting value, '" + args.sort + "'. Continuing with previous value.")
        print("Acceptable sorting values are as follows: ")
        for entry in SORT_INPUTS:
            print(entry)
if args.percent:
    save_obj(args.percent, THRESHOLD_PICKLE_NAME)

def startPicks():
        percentThreshold = load_obj(THRESHOLD_PICKLE_NAME)
        sortPrefix = load_obj(SORTING_PICKLE_NAME)
        heroAdvantageDict = load_obj(ADV_PICKLE_NAME)
        shortDict = load_obj(SHORTHAND_PICKLE_NAME)
        pickedHeroes = []
        heroAdvMap, heroesLeft = initHeroAdvs()
        performSort(heroesLeft, heroAdvMap, pickedHeroes, sortPrefix)
        while (len(pickedHeroes) < 5):
                print("\n")
                commands = input("Enter picked hero, 'sort,' to sort current, or 'q' to quit: ").lower()
                commands = commands.split(",")
                for pickedHero in commands:
                        pickedHero = pickedHero.strip()
                        if (len(pickedHeroes) == 5):
                                break
                        elif (pickedHero == KILL_COMMAND):
                                exit()
                        elif(pickedHero == ""):
                                performSort(heroesLeft, heroAdvMap, pickedHeroes, sortPrefix)
                        elif (pickedHero in SORT_INPUTS):
                                print("Not currently in sorting function. Enter 'sort' with a sort command to sort current data.")
                        elif (pickedHero[:4] == "undo"):
                                undoCommand = pickedHero.split(" ")
                                if (len(undoCommand) == 1):
                                        properHero = pickedHeroes[-1]
                                else:
                                        properHero, shortDict = findHero(undoCommand[1], shortDict, pickedHeroes)
                                if (properHero is not None):
                                        pickedHeroes, heroesLeft, heroAdvMap = undoPick(properHero, 
                                                                                        pickedHeroes, 
                                                                                        heroesLeft, 
                                                                                        heroAdvantageDict, 
                                                                                        heroAdvMap, 
                                                                                        percentThreshold, 
                                                                                        sortPrefix)
                                else:
                                        print(properHero + " not present in picked heroes. Try again.")
                        elif (pickedHero[:6] == "repick"):
                                repickedCommand = pickedHero.split(" ")
                                if (len(repickedCommand) != 3):
                                        print("Insufficient arguments to repick command.")
                                else:
                                        properRemoveHero, shortDict = findHero(repickedCommand[1], shortDict, pickedHeroes)
                                        properPickHero, shortDict = findHero(repickedCommand[2], shortDict, [hero for hero in HEROES_LIST if hero not in pickedHeroes])
                                        if (properRemoveHero is not None):
                                                if (properPickHero is not None):
                                                        pickedHeroes, heroesLeft, heroAdvMap = undoPick(properRemoveHero, 
	                                                                                                    pickedHeroes, 
	                                                                                                    heroesLeft, 
	                                                                                                    heroAdvantageDict, 
	                                                                                                    heroAdvMap, 
	                                                                                                    percentThreshold, 
	                                                                                                    sortPrefix)
                                                        pickedHeroes, heroesLeft, heroAdvMap, shortDict = pickHero(properPickHero, 
                                                                                                                                                                           shortDict, 
                                                                                                                                                                           pickedHeroes, 
                                                                                                                                                                           heroesLeft, 
                                                                                                                                                                           heroAdvantageDict, 
                                                                                                                                                                           heroAdvMap, 
                                                                                                                                                                           percentThreshold, 
                                                                                                                                                                           sortPrefix)
                                                else:
                                                        print("Invalid hero to pick in place of hero you are removing.")
                                        else:
                                                print("Invalid hero to remove.")
                        elif (pickedHero[:4] == "find"):
                                properHero, shortDict = findHero(pickedHero[4:].strip(), shortDict, heroesLeft)
                                if (properHero is not None):
                                        if (properHero in heroesLeft):
                                                print("Finding " + properHero)
                                                performSort([properHero], heroAdvMap, pickedHeroes, sortPrefix)
                                        else:
                                                print("Hero not left in remaining hero pool. Ill advised to pick.")
                                else:
                                        print("Invalid hero to search.")
                        elif (pickedHero[:4] == "sort"):
                                sortTokens = pickedHero.split(' ')
                                if (len(sortTokens) == 1):
                                        print("Enter a sorting command (sum, average, 1-5) as well.")
                                else:
                                        performSort(heroesLeft, heroAdvMap, pickedHeroes, sortTokens[1])
                        elif (pickedHero[:5] == "focus"):
                                focusTokens = pickedHero.split(" ")
                                if ((len(focusTokens) > 1) and (focusTokens[1] in ROLES_NAMES)):
                                        heroesLeft = focusRemainingHeroPool(focusTokens[1], heroesLeft, heroAdvMap, pickedHeroes, sortPrefix)
                        elif ((pickedHero[:3].lower() == BAN_COMMAND) and (pickedHero[3].lower() != 'e')):
                                heroesLeft = banHero(pickedHero, shortDict, heroesLeft, heroAdvMap, pickedHeroes, sortPrefix)
                        else:
                                pickedHeroes, heroesLeft, heroAdvMap, shortDict= pickHero(pickedHero, 
                                                                                          shortDict, 
                                                                                          pickedHeroes, 
                                                                                          heroesLeft, 
                                                                                          heroAdvantageDict, 
                                                                                          heroAdvMap, 
                                                                                          percentThreshold, 
                                                                                          sortPrefix)
        while (True):
                print("Enter " + KILL_COMMAND + " at any time to quit sorting.")
                sortOption = input("\n\nEnter sorting method (" + SORT_INPUTS[0] + ", " + SORT_INPUTS[1] + ", or 1-5): ").lower()
                if (sortOption == KILL_COMMAND):
                        break
                performSort(heroesLeft, heroAdvMap, pickedHeroes, sortOption)

startPicks()