from fileOperators import splitFileByNewline

""" File containing all hero names with one on each line. """
HERONAME_FILE = 'data/heroes'

""" File containing all matchup information for every hero against every other hero. """
MATCHES_FILE = 'data/heromatch'

""" File containing all pre-determined shorthands for the available heroes. """
SHORTHAND_FILE = 'data/shorthands'

""" List containing all possible inputs when sorting the available advantage data after a hero is picked. """
SORT_INPUTS = ['sum', 'average', '1', '2', '3', '4', '5']

""" Input informing the program to exit the current task without resorting to syscalls. """
KILL_COMMAND = "q"

""" Name of the object file containing the serialized data for our hero matchup dictionary. """
ADV_PICKLE_NAME = "heromatchups"

""" Name of the object file containing the serialized data for our shorthand dictionary. """
SHORTHAND_PICKLE_NAME = "shorthands"

""" Shorthand for input to remove a hero from the pool of heroes able to be picked without considering
        it a picked hero for the opposing team. """
BAN_COMMAND = "ban"

""" List of all banned strings that are not allowed to be used as keys in our shorthand dictionary. """
SHORTHAND_BLACKLIST = SORT_INPUTS + [BAN_COMMAND, SHORTHAND_PICKLE_NAME, ADV_PICKLE_NAME, KILL_COMMAND]

""" Name of the serialized object containing the sorting preference. """
SORTING_PICKLE_NAME = "sortPreference"

""" Name of the serialized object containing the percent threshold for pruning heroes. """
THRESHOLD_PICKLE_NAME = "percentThreshold"

""" List containing all hero names. """
HEROES_LIST = splitFileByNewline(HERONAME_FILE)

""" Names of the hero roles files. """
ROLES_NAMES = ["carry", "disabler", "initiator", "jungler", "support", "tank", "nuker", "pusher", "escape"]
