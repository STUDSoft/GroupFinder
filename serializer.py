import pickle


def save(obj, filename):
    with open(filename, "wb") as fp:
        pickle.dump(obj, fp)


def read(filename):
    with open(filename, "rb") as fp:
        obj = pickle.load(fp)
    return obj