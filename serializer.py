import pickle


def save(obj):
    with open('dataset.gfd', 'wb') as fp:
        pickle.dump(obj, fp)


def read():
    with open('dataset.gfd', 'rb') as fp:
        obj = pickle.load(fp)
    return obj
