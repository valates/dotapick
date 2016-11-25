import sys
import argparse
from constantNames import THRESHOLD_PICKLE_NAME, SORTING_PICKLE_NAME, ADV_PICKLE_NAME, SHORTHAND_PICKLE_NAME, KILL_COMMAND, ROLES_NAMES, SORT_INPUTS, INTERNAL_COMMANDS, INTERNAL_HELP_OUTPUT
from pickleSerializers import save_obj, load_obj
from heroFileFormatter import pull_dotabuff
from sorting import perform_sort
from shorthand import reset_shorthands
from heroes import init_hero_advs, find_hero, pick_hero, ban_hero,  undo_pick, repick, focus_remaining_hero_pool, add_to_shorthands

#ALLOW TO NOT ADD TO SHORTHANDS


def main(args):
    args = format_args()
    if args.dotabuff:
        pull_dotabuff()
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
    if args.addshorthand:
        add_to_shorthands(args.addshorthand, load_obj(SORTING_PICKLE_NAME))
    if args.reset:
        save_obj(2.0, THRESHOLD_PICKLE_NAME)
        save_obj(SORT_INPUTS[-1], SORTING_PICKLE_NAME)
        reset_shorthands()
    if args.zeta:
        return
    start_picks()


""" Beings the pick phase of the available heroes. """


def start_picks():
    percent_threshold = load_obj(THRESHOLD_PICKLE_NAME)
    sort_option = load_obj(SORTING_PICKLE_NAME)
    hero_advantage_dict = load_obj(ADV_PICKLE_NAME)
    short_dict = load_obj(SHORTHAND_PICKLE_NAME)
    picked_heroes = []
    hero_adv_map, heroes_left = init_hero_advs()
    perform_sort(heroes_left, hero_adv_map, picked_heroes, sort_option)
    while (True):
        print("\n")
        commands = input("Enter commmand: ").lower()
        commands = commands.split(",")
        for command in commands:
            output_done = False
            command = command.strip()
            if (command != ''):
                if (command == KILL_COMMAND):
                    return
                elif (command == INTERNAL_COMMANDS[0]):
                    internal_help()
                    output_done = True
                elif (command[:4] == INTERNAL_COMMANDS[1]):
                    if (len(picked_heroes) != 0):
                        picked_heroes, heroes_left, hero_adv_map = undo_pick(command.split(" "),
                                                                             short_dict,
                                                                             picked_heroes,
                                                                             heroes_left,
                                                                             hero_advantage_dict,
                                                                             hero_adv_map,
                                                                             percent_threshold)
                elif (command[:6] == INTERNAL_COMMANDS[2]):
                    picked_heroes, heroes_left, hero_adv_map, short_dict = repick(command.split(" "),
                                                                                  short_dict,
                                                                                  picked_heroes,
                                                                                  heroes_left,
                                                                                  hero_advantage_dict,
                                                                                  hero_adv_map,
                                                                                  percent_threshold)
                elif (command[:4] == INTERNAL_COMMANDS[3]):
                    proper_hero, short_dict = find_hero(command[4:].strip(), short_dict, heroes_left)
                    if (proper_hero is not None):
                        print("Finding " + proper_hero)
                        perform_sort([proper_hero], hero_adv_map,
                                     picked_heroes, sort_option)
                        print(str(len(heroes_left)) + " heroes remaining.")
                        output_done = True
                    else:
                        print("Hero not left in remaining hero pool. \
                               Ill advised to pick.")
                elif (command in SORT_INPUTS):
                    perform_sort(heroes_left, hero_adv_map, picked_heroes,
                                 command)
                    print(str(len(heroes_left)) + " heroes remaining.")
                    output_done = True
                elif (command[:5] == INTERNAL_COMMANDS[4]):
                    focus_tokens = command.split(" ")
                    if (len(focus_tokens) > 1) and (focus_tokens[1] in ROLES_NAMES):
                        heroes_left = focus_remaining_hero_pool(focus_tokens[1],
                                                                heroes_left,
                                                                hero_adv_map,
                                                                picked_heroes)
                elif ((command[:3].lower() == INTERNAL_COMMANDS[5]) and (command[3].lower() != 'e')):
                    heroes_left = ban_hero(command, short_dict, heroes_left)
                elif (len(picked_heroes) < 5):
                    picked_heroes, heroes_left, hero_adv_map, short_dict = pick_hero(command,
                                                                                     short_dict,
                                                                                     picked_heroes,
                                                                                     heroes_left,
                                                                                     hero_advantage_dict,
                                                                                     hero_adv_map,
                                                                                     percent_threshold)
                else:
                    if (len(picked_heroes) == 5):
                        str_append = "The maximum number of heroes have \
                                      been picked"
                    else:
                        str_append = "Invalid user input."
                    print("COMMAND BLOCKED: " + str_append)
                if (len(picked_heroes) > 0):
                    if (output_done is False):
                        perform_sort(heroes_left, hero_adv_map, picked_heroes, sort_option)
                        print(str(len(heroes_left)) + " heroes remaining.")
                    print("\n\nPicked heroes:")
                    for hero in picked_heroes:
                        print(hero)
                    print("\n**********\n")


def format_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dotabuff",
                        help="Pulls hero data from dotabuff",
                        action="store_true")
    parser.add_argument("-r", "--reset",
                        help="Sets the percent threshold back to 2.0, resets \
                        sorting setting to default to alphabet sorting, and \
                        removes all user created shorthands.",
                        action="store_true")
    parser.add_argument("-s", "--sort", type=str,
                        help="Changes the default sorting option to one specified. \
                        Sorts by alphabet if no input argument.")
    parser.add_argument("-p", "--percent", type=float,
                        help="Changes the percent threshold above which opposing \
                        heroes are pruned. For each picked hero, any hero \
                        the picked hero has a percent advantage > our \
                        percent threshold is pruned.")
    parser.add_argument("-a", "--addshorthand", type=str,
                        help="Takes a string shorthand as input and allows the user to \
                        assign that shorthand to a hero before picking \
                        beings.")
    parser.add_argument("-z", "--zeta",
                        help="If this specifier is present, does not proceed \
                        to picking phase.",
                        action="store_true")
    return parser.parse_args()


def internal_help():
    print("\n\n")
    for line in INTERNAL_HELP_OUTPUT:
        print(line)


if __name__ == '__main__':
    main(sys.argv)
