import time

from utils.utils import read_dat, min_edit_distance

import nltk
from nltk.corpus import wordnet

def main():
    ok = nltk.download("wordnet")
    if not ok:
        print("not ok")
        return
    tokens_pair = read_dat("data/missp.dat")
    # dist = min_edit_distance(tokens_pair[0][0], tokens_pair[0][1])
    # print(dist)
    wn = wordnet.words(lang='eng')
    print("good")
    # find_distance_naive(wn, tokens_pair)
    print(len(list(wn)))
    # len(wn)
    # for w in wn:
    #     i += 1
    #     print(w)
    #     if i == 10:
    #         break


def find_distance_naive(dictionary, token_set):
    start = time.time()
    for i, word in enumerate(dictionary):
        if i > 10:
            break
        for t in token_set:
            _ = min_edit_distance(t[1], word)
    end = time.time()
    print(end-start)


if __name__ == '__main__':
    main()
