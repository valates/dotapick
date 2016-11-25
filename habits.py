from fileOperators import split_file_by_newline, get_files_in_path
import os
import argparse
import sys


UPPERCASES = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALL_PASS = ['False', 'True', 'None']


def main(args):
    args = format_args()
    if args.directory:
        searching_dir = args.directory
    else:
        searching_dir = os.getcwd()
    files = get_files_in_path(searching_dir)
    for file in files:
        correct_case(file)


def is_constant(token):
    return token.upper() == token


def is_class_name(tokenized_line, token):
    assert token in tokenized_line
    if (tokenized_line[0] == "class"):
        return True
    if ("." in token):
        return True
    token_index = tokenized_line.index(token)
    if (token_index != 0):
        if (len(token) > 0):
            first_char_upper = token[0].upper() == token[0]
        else:
            first_char_upper = False
        after_assignment = tokenized_line[(token_index - 1)] == "="
        return first_char_upper and after_assignment
    return False


def is_module_name(tokenized_line, token):
    assert token in tokenized_line
    if ("import" in tokenized_line):
        if (len(tokenized_line) > 1):
            if ("from" in tokenized_line):
                import_index = tokenized_line.index("import")
                return tokenized_line.index(token) < import_index
            else:
                return tokenized_line.index(token) > 0
    return False


def syntax_characters(word):
    assert type(word) == str
    replacement_word = ''
    for character in word:
        if character in UPPERCASES:
            replacement_word += ('_' + character.lower())
        else:
            replacement_word += character
    return replacement_word


def correct_case(filename):
    lines = split_file_by_newline(filename)
    in_block_comment = False
    if (filename != "habits.py") and (filename[-3:] == ".py"):
        with open('tmp', 'a') as f:
            for line in lines:
                corrected_line = ''
                tokenized_line = line.split(" ")
                for token in tokenized_line:
                    if (token == '"""'):
                        in_block_comment = not in_block_comment
                    if (not in_block_comment):
                        class_name = is_class_name(tokenized_line, token)
                        mod_name = is_module_name(tokenized_line, token)
                        cnst_name = is_constant(token)
                        if not class_name and not mod_name and not cnst_name:
                            token = syntax_characters(token)
                    corrected_line += (token + ' ')
                corrected_line = corrected_line[:-1]
                corrected_line = corrected_line.replace('_false', 'False')
                corrected_line = corrected_line.replace('_true', 'True')
                corrected_line = corrected_line.replace('_none', 'None')
                f.write(corrected_line + "\n")
        os.remove(filename)
        os.rename('tmp', filename)


def format_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", type=str,
                        help="Takes a string shorthand as input and allows \
                        the user to assign that shorthand to a hero before \
                        picking beings.")
    return parser.parse_args()


if __name__ == '__main__':
    main(sys.argv)
