import pickle

""" Serializes an object in a subdirectory, "/obj" with filename, FILENAME.
        Uses .pkl extension. """


def save_obj(obj, filename):
    with open('obj/' + filename + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


""" Unserializes an object in a subdirectory, "/obj" with filename, FILENAME.
        Uses .pkl extension. """


def load_obj(filename):
    with open('obj/' + filename + '.pkl', 'rb') as f:
        return pickle.load(f)
