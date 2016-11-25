from os import listdir
from os.path import isfile, join, exists


""" For a file with string name FILENAME, splits the contents based on the
    newline delimiter and returns the split lines as a list. """


def split_file_by_newline(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    return lines


""" For a file with string name FILENAME, collects each line which is of the
    form 'A, B, C, D, ... Z. For all values in the line excluding A (the
    first string before a comma), a key value pair is made where !A is
    paired with A. The key, value pair is added to a dictionary and the
    dictionary is returned after each line has been parsed in this manner. """


def form_dict_from_comma_file(filename):
    lines = split_file_by_newline(filename)
    comma_lists = []
    for line in lines:
        line_list = line.split(', ')
        if (len(line_list) != 1):
            comma_lists.append(line_list)
    cur_dict = {}
    for entry in comma_lists:
        list_keys = entry[1:]
        list_val = entry[0]
        for cur_key in list_keys:
            if cur_key not in cur_dict:
                cur_dict[cur_key] = list_val
    return cur_dict


""" Returns all files in a directory specified by PATH. """


def get_files_in_path(path):
    assert exists(path)
    return [file for file in listdir(path) if isfile(join(path, file))]
