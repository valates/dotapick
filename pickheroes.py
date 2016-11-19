import argparse
from constantNames import THRESHOLD_PICKLE_NAME, SORTING_PICKLE_NAME, SORTING_PICKLE_NAME, ADV_PICKLE_NAME, SHORTHAND_PICKLE_NAME, KILL_COMMAND, ROLES_NAMES, SORT_INPUTS, HEROES_LIST, INTERNAL_COMMANDS
from pickleSerializers import save_obj, load_obj
from heroFileFormatter import pullDotabuff
from sorting import performSort
from shorthand import resetShorthands
from heroes import initHeroAdvs, findHero, pickHero, banHero,  undoPick, repick, focusRemainingHeroPool

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dotabuff", 
                    help="Pulls hero data from dotabuff",
                    action="store_true")
parser.add_argument("-r", "--reset",         
                    help="Sets the percent threshold back to 2.0, resets sorting \
                    setting to default to alphabet sorting, and removes all user \
                    created shorthands.",
                    action="store_true")
parser.add_argument("-s", "--sort", type=str,
                    help="Changes the default sorting option to one specified. \
                    Sorts by alphabet if no input argument.")
parser.add_argument("-p", "--percent", type=float,
                    help="Changes the percent threshold above which opposing \
                    heroes are pruned. For each picked hero, any hero the picked \
                    hero has a percent advantage > our percent threshold is pruned.")

args = parser.parse_args()
if args.dotabuff:
    pullDotabuff()
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
if args.reset:
    save_obj(2.0, THRESHOLD_PICKLE_NAME)
    save_obj(SORT_INPUTS[-1], SORTING_PICKLE_NAME)
    resetShorthands()

def startPicks():
    percentThreshold = load_obj(THRESHOLD_PICKLE_NAME)
    sortOption = load_obj(SORTING_PICKLE_NAME)
    heroAdvantageDict = load_obj(ADV_PICKLE_NAME)
    shortDict = load_obj(SHORTHAND_PICKLE_NAME)
    pickedHeroes = []
    heroAdvMap, heroesLeft = initHeroAdvs()
    performSort(heroesLeft, heroAdvMap, pickedHeroes, sortOption)
    while (True):
        print("\n")
        commands = input("Enter commmand: ").lower() #TODO replace with actual help AND some form of help if loop
        commands = commands.split(",")
        for command in commands:
            command = command.strip()
            if (command != ''):
                if (command == KILL_COMMAND):
                    exit()
                elif (command[:4] == INTERNAL_COMMANDS[0]):
                    if (len(pickedHeroes) != 0):
                        pickedHeroes, heroesLeft, heroAdvMap = undoPick(command.split(" "), 
                                                                          shortDict, 
                                                                          pickedHeroes, 
                                                                          heroesLeft, 
                                                                          heroAdvantageDict, 
                                                                          heroAdvMap, 
                                                                          percentThreshold, 
                                                                          sortOption)
                elif (command[:6] == INTERNAL_COMMANDS[1]):
                    pickedHeroes, heroesLeft, heroAdvMap, shortDict = repick(command.split(" "), 
                                                                             shortDict,
                                                                             pickedHeroes, 
                                                                             heroesLeft, 
                                                                             heroAdvantageDict, 
                                                                             heroAdvMap, 
                                                                             percentThreshold, 
                                                                             sortOption)
                elif (command[:4] == INTERNAL_COMMANDS[2]):
                    properHero, shortDict = findHero(command[4:].strip(), shortDict, heroesLeft)
                    if (properHero is not None):
                        if (properHero in heroesLeft):
                            print("Finding " + properHero)
                            performSort([properHero], heroAdvMap, pickedHeroes, sortOption)
                        else:
                            print("Hero not left in remaining hero pool. Ill advised to pick.")
                    else:
                        print("Invalid hero to search.")
                elif (command in SORT_INPUTS):
                    performSort(heroesLeft, heroAdvMap, pickedHeroes, command)
                elif (command[:4] == INTERNAL_COMMANDS[3]):
                    sortTokens = command.split(' ')
                    if (len(sortTokens) == 1):
                        print("Enter a sorting command (sum, average, 1-5, alpha) as well.")
                    else:
                        performSort(heroesLeft, heroAdvMap, pickedHeroes, sortTokens[1])
                elif (command[:5] == INTERNAL_COMMANDS[4]):
                    focusTokens = command.split(" ")
                    if ((len(focusTokens) > 1) and (focusTokens[1] in ROLES_NAMES)):
                        heroesLeft = focusRemainingHeroPool(focusTokens[1], heroesLeft, heroAdvMap, pickedHeroes, sortOption)
                elif ((command[:3].lower() == INTERNAL_COMMANDS[5]) and (command[3].lower() != 'e')):
                    heroesLeft = banHero(command, shortDict, heroesLeft, heroAdvMap, pickedHeroes, sortOption)
                elif (len(pickedHeroes) < 5):
                    pickedHeroes, heroesLeft, heroAdvMap, shortDict = pickHero(command, 
                                                                               shortDict, 
                                                                               pickedHeroes, 
                                                                               heroesLeft, 
                                                                               heroAdvantageDict, 
                                                                               heroAdvMap, 
                                                                               percentThreshold, 
                                                                               sortOption)
                    if (len(pickedHeroes) == 5):
                        print("The maximum number of heroes have been picked")
                else:
                    print("COMMAND BLOCKED: Invalid user input.")

startPicks()