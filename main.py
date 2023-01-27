
from utils.utils import read_dat, min_edit_distance

import nltk


def main():
    ok = nltk.download("wordnet")
    if not ok:
        print("not ok")
        return
    tokens_pair = read_dat("data/missp.dat")
    dist = min_edit_distance(tokens_pair[0][0], tokens_pair[0][1])
    print(dist)


if __name__ == '__main__':
    main()
