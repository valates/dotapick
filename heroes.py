from constantNames import HEROES_LIST
from shorthand import add_shorthand
from nameFormatter import proper_format_name
from fileOperators import split_file_by_newline
from nameFormatter import prophet_fix


""" Initializes a blank dictionary to represent advantages
    each picked hero has against the remaining heroes and a
    blank list to represent all heroes left to pick from. """


def init_hero_advs():
    hero_adv_map = {}
    heroes_left = []
    for hero in HEROES_LIST:
        hero_adv_map[hero] = []
        heroes_left.append(hero)
    return hero_adv_map, heroes_left


""" Searches for the specified hero with name PICKEDHERO
    first in the dictionary of shorthands, SHORTDICT, and
    once a hero has been located in shorthands or the list
    of heroes. Once the hero has been located, we check if its
    proper name is located in the specified list of some
    group of heroes, HEROESTOCHECKFORPICK. If present, the
    hero is returned. Otherwise, None is returned. """


def find_hero(picked_hero, short_dict, heroes_to_check_for_pick):
    if (picked_hero in short_dict):
        proper_hero = short_dict[picked_hero]
    elif(picked_hero.lower() in short_dict):
        proper_hero = short_dict[picked_hero.lower()]
    else:
        proper_hero = proper_format_name(picked_hero)
    if (proper_hero not in HEROES_LIST):
        proper_hero, short_dict = add_to_shorthands(picked_hero, short_dict)
    if (heroes_to_check_for_pick != HEROES_LIST) and (proper_hero not in heroes_to_check_for_pick):
        return None, short_dict
    return proper_hero, short_dict


""" Picks the hero specified by string PICKEDHERO. Takes the
    dictionary of shorthands, SHORTDICT, as well as the list
    of picked heroes, PICKEDHEROES and adds the picked hero
    to it. We also pass the dictionary of advantages picked
    heroes have against the remaining heroes, HEROADVANTAGEDICT,
    the mapping of advantages each hero has against all other heroes,
    HEROADVMAP, the threshold above which a hero is considered highly
    advantaged, PERCENTTHRESHOLD, and the storing specifier, SORTPREFIX. """


def pick_hero(picked_hero, short_dict, picked_heroes, heroes_left,
              hero_advantage_dict, hero_adv_map, percent_threshold):
    proper_hero, short_dict = find_hero(picked_hero, short_dict, HEROES_LIST)
    if (proper_hero is not None):
        picked_heroes, heroes_left, hero_adv_map = perform_advantage_search(proper_hero,
                                                                            picked_heroes,
                                                                            heroes_left,
                                                                            hero_advantage_dict,
                                                                            hero_adv_map,
                                                                            percent_threshold)
    return picked_heroes, heroes_left, hero_adv_map, short_dict


""" Removes the hero specified by string PICKEDHERO from the list of remaining
    heroes, HEROESLEFT. """


def ban_hero(picked_hero, short_dict, heroes_left, checked_against, captains=False):
    if (not captains):
        picked_hero = picked_hero[3:]
    proper_hero, short_dict = find_hero(picked_hero.strip(), short_dict, checked_against)
    if (proper_hero is not None):
        if proper_hero in heroes_left:
            heroes_left.remove(proper_hero)
        print(proper_hero + " banned.")
    else:
        print("'" + picked_hero + "' not present in hero list. Try again.")
    return heroes_left


""" Removes the specified hero from pickedHeroes based on undoCmd. If undoCmd
    is simply "undo", the last hero picked is removed. Updates the heroesLeft
    list accordingly. """


def undo_pick(undo_cmd, short_dict, picked_heroes, heroes_left,
              hero_advantage_dict, hero_adv_map, percent_threshold):
    if (len(undo_cmd) == 1):
        proper_hero = picked_heroes[-1]
    else:
        proper_hero, short_dict = find_hero(undo_cmd[1], short_dict,
                                            picked_heroes)
    if (proper_hero is not None):
        picked_heroes, heroes_left, hero_adv_map = undo_helper(proper_hero,
                                                               picked_heroes,
                                                               heroes_left,
                                                               hero_advantage_dict,
                                                               hero_adv_map,
                                                               percent_threshold)
    else:
        print(proper_hero + " not present in picked heroes. Try again.")
    return picked_heroes, heroes_left, hero_adv_map


""" Removes the hero specificied by PROPERHERO from the list of picked heroes,
    PICKEDHEROES. Updates the list of remaining heroes accordingly (i.e., reads
    the heroes that are no longer considered highly disadvantaged). """


def undo_helper(proper_hero, picked_heroes, heroes_left, hero_advantage_dict,
                hero_adv_map, percent_threshold):
    picked_heroes.remove(proper_hero)
    hero_adv_map, heroes_left = init_hero_advs()
    picked_copy = []
    for hero in picked_heroes:
        picked_copy, heroes_left, hero_adv_map = perform_advantage_search(hero,
                                                                          picked_copy,
                                                                          heroes_left,
                                                                          hero_advantage_dict,
                                                                          hero_adv_map,
                                                                          percent_threshold)
    return picked_copy, heroes_left, hero_adv_map


""" Replaces a hero in the list of picked heroes, PICKEDHEROES, with a yet
    unpicked hero based on the string specifier REPICKCMD. """


def repick(repick_cmd, short_dict, picked_heroes, heroes_left,
           hero_advantage_dict, hero_adv_map, percent_threshold):
    if (len(repick_cmd) != 3):
        print("Insufficient arguments to repick command.")
    else:
        proper_remove_hero, short_dict = find_hero(repick_cmd[1], short_dict,
                                                   picked_heroes)
        proper_pick_hero, short_dict = find_hero(repick_cmd[2], short_dict,
                                                 [hero for hero in HEROES_LIST if hero not in picked_heroes])
        if (proper_remove_hero is not None):
            if (proper_pick_hero is not None):
                picked_heroes, heroes_left, hero_adv_map = undo_helper(proper_remove_hero,
                                                                       picked_heroes,
                                                                       heroes_left,
                                                                       hero_advantage_dict,
                                                                       hero_adv_map,
                                                                       percent_threshold)
                picked_heroes, heroes_left, hero_adv_map, short_dict = pick_hero(proper_pick_hero,
                                                                                 short_dict,
                                                                                 picked_heroes,
                                                                                 heroes_left,
                                                                                 hero_advantage_dict,
                                                                                 hero_adv_map,
                                                                                 percent_threshold)
            else:
                print("Invalid hero to pick in place of hero \
                       you are removing.")
        else:
            print("Invalid hero to remove.")
    return picked_heroes, heroes_left, hero_adv_map, short_dict


""" Takes the string name for a file listing heroes fitting a specific role.
        Removes all heroes from the remaining hero list that do not have their
        name in the corresponding role file specified by string
        FOCUSSPECIFIER. """


def focus_remaining_hero_pool(focus_specifier, heroes_left, hero_adv_map,
                              picked_heroes):
    to_focus = split_file_by_newline("data/" + focus_specifier)
    heroes_left = [hero for hero in heroes_left if hero in to_focus]
    return heroes_left


""" Searches the mapping of each hero's advantage to every other hero stored
    in HEROADVMAP. For each hero in the list of remaining heroes, HEROESLEFT,
    remove that hero if the picked hero specified by PROPERHERO has an
    advantage against the hero in HEROESLEFT greater than or equal to
    PERCENTTHRESHOLD. """


def perform_advantage_search(proper_hero, picked_heroes, heroes_left,
                             hero_advantage_dict, hero_adv_map,
                             percent_threshold):
    print("\n**********\n")
    if (proper_hero not in picked_heroes):
        if proper_hero in heroes_left:
            heroes_left.remove(proper_hero)
        hero_advs = hero_advantage_dict[proper_hero]
        for entry_tuple in hero_advs:
            entry_name = entry_tuple[0]
            entry_name = prophet_fix(entry_name)
            entry_adv = float(entry_tuple[1])
            hero_adv_map[entry_name].append(entry_adv)
            if (entry_adv > percent_threshold):
                if (entry_name in heroes_left):
                    heroes_left.remove(entry_name)
        picked_heroes.append(proper_hero)
    else:
        print("Hero already marked as picked.")
    return picked_heroes, heroes_left, hero_adv_map


""" Adds the string specified by PICKEDHERO to the shorthand
        dictionary, SHORTDICT. """


def add_to_shorthands(picked_hero, short_dict):
    hero_to_return = None
    print("Invalid hero name '" + picked_hero + "', add it to shorthands?")
    hero_to_map = input("If so, enter a valid hero name (or 'n' to cancel): ")
    if (hero_to_map.lower() != 'n'):
        hero_to_map = proper_format_name(hero_to_map)
        if (hero_to_map not in HEROES_LIST) or (hero_to_map not in short_dict):
            hero_to_map, short_dict = find_hero(hero_to_map, short_dict, HEROES_LIST)
            response = input("Adding shorthand '" + picked_hero + "' for hero '" + hero_to_map + "'. Enter 'y' to confirm: ")
            if (response == 'y'):
                short_dict = add_shorthand(hero_to_map, picked_hero, short_dict)
                hero_to_return = hero_to_map
        else:
            print("Invalid hero name '" + hero_to_map + "', not adding to shorthands. Please enter a real name.")
    return hero_to_return, short_dict
