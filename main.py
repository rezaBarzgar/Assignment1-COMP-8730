import json
import time
from multiprocessing import Pool
from utils.utils import *
import nltk
from nltk.corpus import wordnet
import pytrec_eval


def main():
    wordnet_ = nltk.download("wordnet")
    if not wordnet_:
        print("unable to download Wordnet")
        return
    dictionary = list(wordnet.words(lang='eng'))
    tokens_pairs = read_data("data/missp.dat")
    start = time.time()

    # results = []
    # for item in tokens_pairs[:6]:
    #     results.append(most_similar_words(item, dictionary))
    with Pool(6) as pool:
        args = list(zip(tokens_pairs[:3], [dictionary for i in range(len(tokens_pairs[:3]))]))
        results = pool.starmap(most_similar_words, args)
    print(f'runtime: {time.time() - start}')
    qrel = {}
    for i in range(len(tokens_pairs)):
        qrel[f'{tokens_pairs[i]}'] = {
            'success_at_1': 1,
            'success_at_5': 1,
            'success_at_10': 1
        }
    result_data = {}
    for i in range(len(results)):
        success_at_1, success_at_5, success_at_10 = success_at_k(results[i], tokens_pairs[i])
        result_data[f'{tokens_pairs[i]}'] = {
            'success_at_1': success_at_1,
            'success_at_5': success_at_5,
            'success_at_10': success_at_10
        }

    print(json.dumps(result_data, indent=1))
    for measure in sorted(list(result_data[list(result_data.keys())[0]].keys())):
        print(measure, 'average:', round(pytrec_eval.compute_aggregated_measure(
                  measure, [query_measures[measure] for query_measures in result_data.values()]), 2))


if __name__ == '__main__':
    main()
