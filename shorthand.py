from pickleSerializers import save_obj, load_obj
from fileOperators import form_dict_from_comma_file
from constantNames import SHORTHAND_FILE, SHORTHAND_PICKLE_NAME


""" Creates a dictionary from the file containing all preset hero shorthands
    located in /data/shorthands. Saves the dictionary to a file. """


def form_shorthands():
    short_dict = form_dict_from_comma_file(SHORTHAND_FILE)
    save_obj(short_dict, SHORTHAND_PICKLE_NAME)


""" Associates the string SHORTHAND with the hero with string name HERONAME by
    adding the key, value pair to the dictionary of shorthands, SHORTDICT.
    Returns the resulting dictionary if the key was not already present.
    Returns SHORTDICT untouched if key SHORTHAND is present. """


def add_shorthand(heroname, shorthand, short_dict):
    if shorthand not in short_dict:
        short_dict[shorthand] = heroname
        save_obj(short_dict, SHORTHAND_PICKLE_NAME)
    else:
        print("Shorthand '" + shorthand + "' already present.")
    return short_dict


""" Removes the association between the string SHORTHAND and the hero with
    string name HERONAME by removing the key from the dictionary, SHORTDICT.
    Returns the resulting dictionary if the key was present. Returns SHORTDICT
    untouched if key SHORTHAND is not present. """


def remove_shorthand(shorthand, heroname, short_dict):
    if shorthand in short_dict:
        print("Shorthand '" + shorthand + "' not present.")
    else:
        del short_dict[shorthand]
        save_obj(short_dict, SHORTHAND_PICKLE_NAME)
    return short_dict


""" Creates a new shorthand dictionary and returns it to the caller. If boolean
    FACTORYZERO is True, a blank dictionary is returned. If FACTORYZERO is
    False, the dictioanry matches the contents of /data/shorthands. """


def reset_shorthands(factory_zero=False):
    if factory_zero:
        short_dict = {}
        save_obj(short_dict, SHORTHAND_PICKLE_NAME)
    else:
        form_shorthands()
        short_dict = load_obj(SHORTHAND_PICKLE_NAME)
    return short_dict
