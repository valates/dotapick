#SOURCE: http://stackoverflow.com/questions/19201290/how-to-save-a-dictionary-to-a-file-in-python

import pickle

def save_obj(obj, filename):
    with open('obj/'+ filename + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(filename):
    with open('obj/' + filename + '.pkl', 'rb') as f:
        return pickle.load(f)