import json
import time
from utils.utils import *
import nltk
from multiprocessing import Pool
import pytrec_eval


def main():
    wordnet_ = nltk.download("wordnet")
    if not wordnet_:
        print("unable to download Wordnet")
        return
    tokens_pairs = read_data("data/missp.dat")
    start = time.time()
    with Pool() as pool:
        results = pool.map(most_similar_words, tokens_pairs)

    data = {}
    for i in range(len(results)):
        success_at_1, success_at_5, success_at_10 = success_at_k(results[i], tokens_pairs[i])
        data[f'{tokens_pairs[i]}'] = {
            'success_at_1': success_at_1,
            'success_at_5': success_at_5,
            'success_at_10': success_at_10
        }
    print(data)
    evaluator = pytrec_eval.RelevanceEvaluator(
        data, {'success'})
    print(json.dumps(evaluator.evaluate(data), indent=1))
    print(f'runtime: {time.time() - start}')


if __name__ == '__main__':
    main()
