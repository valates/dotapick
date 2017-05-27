import sys
import argparse
import time
from constantNames import HEROES_LIST, THRESHOLD_PICKLE_NAME, SORTING_PICKLE_NAME, ADV_PICKLE_NAME, SHORTHAND_PICKLE_NAME, KILL_COMMAND, BRACKET_PICKLE_NAME, ROLES_NAMES, SORT_INPUTS, INTERNAL_COMMANDS, INTERNAL_HELP_OUTPUT, PICK_BAN_ORDER, CAPTAINS_UNALLOWED_HEROES, UNPLAYABLE_WINRATE
from pickleSerializers import save_obj, load_obj
from heroFileFormatter import pull_dotabuff, get_meta
from sorting import perform_sort
from nameFormatter import proper_format_name
from shorthand import reset_shorthands
from heroes import init_hero_advs, find_hero, pick_hero, ban_hero,  undo_pick, repick, focus_remaining_hero_pool, add_to_shorthands


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
        form_shorthands()
    if args.meta:
        get_meta()
        meta_to_prune = load_obj(BRACKET_PICKLE_NAME)
        #Each desired skill bracket will go one beyond in each direction, to account for border games
        args.meta = args.meta.replace('overall', '6')
        args.meta = args.meta.replace('all', '6')
        args.meta = args.meta.replace('ns', '1,2,3')
        args.meta = args.meta.replace('vhs', '3')
        args.meta = args.meta.replace('hs', '4,5')
        desired_brackets = args.meta.split(',')
        brackets_to_remove = [1, 2, 3, 4, 5, 6]
        for entry in desired_brackets:
            brackets_to_remove.remove(int(entry))
        for hero in meta_to_prune:
            cur_hero = meta_to_prune[hero]
            pop_shift = 1
            for entry in brackets_to_remove:
                cur_hero.pop(entry - pop_shift)
                pop_shift += 1
        save_obj(meta_to_prune, BRACKET_PICKLE_NAME)
    else:
        save_obj({}, BRACKET_PICKLE_NAME)
    if args.zeta:
        return
    elif args.captain:
        captains_mode(args.captain)
    else:
        start_picks()


""" Beings the pick phase of the available heroes. """


def start_picks():
    percent_threshold = load_obj(THRESHOLD_PICKLE_NAME)
    sort_option = load_obj(SORTING_PICKLE_NAME)
    hero_advantage_dict = load_obj(ADV_PICKLE_NAME)
    short_dict = load_obj(SHORTHAND_PICKLE_NAME)
    picked_heroes = []
    hero_adv_map, heroes_left = init_hero_advs()
    meta_trends = load_obj(BRACKET_PICKLE_NAME)
    for entry in meta_trends:
        brackets_of_hero = meta_trends[entry]
        for val in brackets_of_hero:
            if (val <= UNPLAYABLE_WINRATE):
                heroes_left.remove(entry)
                break
    suppress_hero_list = False
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
                    not_banned = [hero for hero in HEROES_LIST if hero not in picked_heroes]
                    heroes_left = ban_hero(command, short_dict, heroes_left, not_banned)
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


def captains_mode(starter):
    #may need a ban list
    first_actor = starter
    if (starter == 'Radiant'):
        second_actor = 'Dire'
    else:
        second_actor = 'Radiant'
    percent_threshold = load_obj(THRESHOLD_PICKLE_NAME)
    sort_option = load_obj(SORTING_PICKLE_NAME)
    hero_adv_dict = load_obj(ADV_PICKLE_NAME)
    short_dict = load_obj(SHORTHAND_PICKLE_NAME)
    banned_heroes = []
    heroes_picked_first = []
    heroes_picked_second = []
    hero_adv_map_first, heroes_left_first = init_hero_advs()
    hero_adv_map_second, heroes_left_second = init_hero_advs()

    for hero in CAPTAINS_UNALLOWED_HEROES:
        heroes_left_first.remove(hero)
        heroes_left_second.remove(hero)
    for action in PICK_BAN_ORDER:
        #add typo/nothing picked or banned handler
        #add repick support? probably not
        actor = action % 2
        if (actor == 0):
            actor_str = first_actor
        else:
            actor_str = second_actor #add 'already banned' handler 
        if (action <= 1):
            hero = input(actor_str + "'s ban: ")
            to_check = [hero for hero in HEROES_LIST if hero not in heroes_picked_first]
            to_check = [hero for hero in to_check if hero not in heroes_picked_second]
            heroes_left_first = ban_hero(hero, short_dict, heroes_left_first, to_check, True)
            heroes_left_second = ban_hero(hero, short_dict, heroes_left_second, to_check, True)
            banned_heroes.append(hero) #need a checker...
        else:
            hero = input(actor_str + "'s pick: ")
            picked_heroes = heroes_picked_first + heroes_picked_second
            if (action == 2):
                heroes_left = heroes_left_second
                adv_map = hero_adv_map_second
            else:
                heroes_left = heroes_left_first
                adv_map = hero_adv_map_first
            if hero not in picked_heroes:
                picked_heroes_both, heroes_left_second, adv_map, short_dict = pick_hero(hero,
                                                                                        short_dict,
                                                                                        picked_heroes,
                                                                                        heroes_left,
                                                                                        hero_adv_dict,
                                                                                        adv_map,
                                                                                        percent_threshold)
            if (action == 2):
                heroes_left_second = heroes_left
                hero_adv_map_second = adv_map
                heroes_picked_first = [hero for hero in picked_heroes if hero not in heroes_picked_second]
            else:
                heroes_left_first = heroes_left
                hero_adv_map_first = adv_map
                heroes_picked_second = [hero for hero in picked_heroes if hero not in heroes_picked_first]
        if (actor == 0):
            heroes_left = heroes_left_second
            advs = hero_adv_map_second
            picked = heroes_picked_first
        else:
            heroes_left = heroes_left_first
            advs = hero_adv_map_first
            picked = heroes_picked_second
        perform_sort(heroes_left, advs, picked, sort_option)
        print(str(len(heroes_left)) + " heroes remaining.")
        print("\n\n" + actor_str + " picked heroes:")
        for hero in picked:
            print(hero)
        print("\n\nAll banned heroes:")
        for hero in banned_heroes:
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
                        help="Takes a string shorthand as input and allows the user to "
                        "assign that shorthand to a hero before picking "
                        "beings.")
    parser.add_argument("-c", "--captain", type=str,
                        help="Starts captain's mode picking style instead of standard picking mode."
                        "Must specify starting team to get pick/ban order correct.")
    parser.add_argument("-m", "--meta", type=str,
                        help="Pulls metadata from dotabuff. Metadata is the winrate of heroes across \
                        all skill brackets. Requires a bracket specifier of the form 'a,b,c' where \
                        a, b, c are numbers between 1 and 5.")
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
