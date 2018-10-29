import numpy as np


def save_dataset(data, file):
    np.save(file, data)


def load_dataset(file):
    return np.load(file)
