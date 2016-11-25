""" For an inputted string HERONAME, formats the string to represent
    the actual hero's name.
        The formatted string is returned. """


def proper_format_name(heroname):
    proper_hero = ''
    for i in range(0, len(heroname)):
        if (i == 0 or heroname[(i - 1)] in [' ', '-']) and (heroname[i:(i + 2)] != "of") and (heroname[i:(i + 2)] != "th"):
            proper_hero += heroname[i].capitalize()
        else:
            proper_hero += heroname[i]
    return prophet_fix(proper_hero)


""" For an inputted string HERONAME, fixes an edge case where the
    associated heroname after being stored in a Tuple changes from
    "Nature's" to "Natures". The updated string is returned. """


def prophet_fix(heroname):
    return heroname.replace("Natures", "Nature's")
