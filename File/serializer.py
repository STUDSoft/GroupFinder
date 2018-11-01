import numpy as np


def save(data, file):
    np.save(file, data)


def load(file):
    return np.load(file)
