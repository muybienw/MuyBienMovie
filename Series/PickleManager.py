import os
import pickle

import Movie

PATH = '/Users/MuyBien/PycharmProjects/MoviePuff/Series/'

def loadFromPickle(file_name):
    path = PATH + file_name
    if os.path.isfile(path):
        pickle_in = open(path, "rb")
        return pickle.load(pickle_in)
    else:
        return None

def dump(file_name, data):
    path = PATH + file_name
    pickle_out = open(path, "wb")
    pickle.dump(data, pickle_out)
    pickle_out.close()

def main():
    file = 'Film Forum: Ingmar Bergman'
    print loadFromPickle(file)

if __name__ == '__main__':
    main()