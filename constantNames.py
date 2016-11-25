""" For the given input string, TEXT, removes all instances of multiple common
    string artifacts that are present in an HTML string. """


from fileOperators import split_file_by_newline

""" File containing all hero names with one on each line. """
HERONAME_FILE = 'data/heroes'

""" File containing all matchup information for every hero against every other
    hero. """
MATCHES_FILE = 'data/heromatch'

""" File containing all pre-determined shorthands for the available heroes. """
SHORTHAND_FILE = 'data/shorthands'

""" List containing all possible inputs when sorting the available advantage
    data after a hero is picked. """
SORT_INPUTS = ['sum', 'average', '1', '2', '3', '4', '5', 'alpha']

""" Input informing the program to exit the current task without resorting to
    syscalls. """
KILL_COMMAND = "q"

""" Name of the object file containing the serialized data for our hero
    matchup dictionary. """
ADV_PICKLE_NAME = "heromatchups"

""" Name of the object file containing the serialized data for our shorthand
    dictionary. """
SHORTHAND_PICKLE_NAME = "shorthands"

""" Name of the serialized object containing the sorting preference. """
SORTING_PICKLE_NAME = "sortPreference"

""" Name of the serialized object containing the percent threshold for pruning
    heroes. """
THRESHOLD_PICKLE_NAME = "percentThreshold"

""" List containing all hero names. """
HEROES_LIST = split_file_by_newline(HERONAME_FILE)

""" Names of the hero roles files. """
ROLES_NAMES = ["carry", "disabler", "initiator", "jungler", "support", "tank",
               "nuker", "pusher", "escape"]

""" Commands used internally in the function startPicks() in pickHeroes.py.
They're present here to ensure they're all blacklisted from being used as
shorthands."""
INTERNAL_COMMANDS = ["help", "undo", "repick", "find", "focus", "ban"]

""" The directory containing the help output for start_picks() in
    pick_heroes.py. """
INTERNAL_HELP_FILE = "data/internalCommands"

""" _the output supplied at a request for help or invalid user input in
    start_picks(). """
INTERNAL_HELP_OUTPUT = split_file_by_newline(INTERNAL_HELP_FILE)

""" List of all banned strings that are not allowed to be used as keys in our
    shorthand dictionary. """
SHORTHAND_BLACKLIST = SORT_INPUTS + ROLES_NAMES + HEROES_LIST + INTERNAL_COMMANDS + INTERNAL_HELP_FILE
SHORTHAND_BLACKLIST += [SHORTHAND_PICKLE_NAME, ADV_PICKLE_NAME, KILL_COMMAND, SHORTHAND_FILE, MATCHES_FILE]
SHORTHAND_BLACKLIST += [SORTING_PICKLE_NAME, THRESHOLD_PICKLE_NAME]
