""" For an input string LINE, finds the first substring between string
    STARTTEXT and string STOPTEXT. Returns the substring minus any HTML
    artificats along with the index of the last character in the substring
    in a tuple. If GIVENULL is True, the string "null" is returned in the
    tuple along with an index of -1. If HALTBRACKETKILLING is True, the
    substrings are added to the list without any text between '<' and '>' being
    removed. If STARTATSTART is True,
    """


def html_searcher(start_text, stop_text, line, give_null=False,
                  halt_bracket_killing=False, start_at_start=False):
    start_index = line.find(start_text)
    start_len = len(start_text)
    if start_at_start:
        line = line[start_index:]
    stop_index = line.find(stop_text)
    hold = 0
    if (stop_index < start_index):
        line = line[start_index + len(start_text):]
        hold = start_index
        start_len = 0
        start_index = 0
        stop_index = line.find(stop_text)
    if ((start_index != -1) and (stop_index != -1)):
        final_text = line[start_index + start_len:stop_index]
        if halt_bracket_killing:
            return (remove_common_artifacts(final_text), stop_index + hold)
        return (remove_common_artifacts(remove_brackets(final_text)), stop_index + hold)
    if (give_null):
        return ("null", -1)
    return None


""" For an input string LINE, finds all substrings within TEXT in between
    string STARTEXT and string STOPTEXT. Returns a list of all such
    substrings. If HALTBRACKETKILLING is True, the substrings are added to
    the list without any text between '<' and '>' being removed. Such text is
    removed if HALTBRACKETKILLING is False. """


def html_search_all(start_text, stop_text, line, halt_bracket_killing=False):
    token_tuple = html_searcher(start_text, stop_text, line, True,
                                halt_bracket_killing)
    tokens = []
    while (token_tuple[1] != -1):
        last_stop = token_tuple[1]
        tokens.append(token_tuple[0])
        line = line[last_stop:]
        token_tuple = html_searcher(start_text, stop_text, line, True, halt_bracket_killing, False)
    return tokens


""" For input string TEXT, remove all characters in between the character '<'
    and '>', inclusive. Does not remove any text until the '<' character
    is encountered. """


def remove_brackets(text):
    len_text = len(text)
    in_brackets = False
    final_text = ""
    for i in range(len_text):
        cur_char = text[i]
        if (cur_char == '<'):
            in_brackets = True
        else:
            if (in_brackets is False):
                final_text += cur_char
            if (cur_char == '>'):
                in_brackets = False
    return final_text


""" For the given input string, TEXT, removes all instances of multiple common
    string artifacts that are present in an HTML string. """


def remove_common_artifacts(text):
    text = text.replace("&nbsp;", "")
    text = text.replace("&quot;", "\"")
    text = text.replace("&#039;", "'")
    text = text.replace("&#39;", "'")
    text = text.replace("&#8217;", "'")
    text = text.replace("&#8220;", "\"")
    text = text.replace("&#8221;", "\"")
    text = text.replace("&amp;", "&")
    text = text.replace("\\", "")
    text = text.replace("<br>ot", " ")
    return text
