import pytrec_eval


def main():
    results = []
    with open("data/output1.dat", "r") as f:
        lines = f.readlines()
        for l in lines:
            incorrect, correct, mask1, mask2 = l.split(",")
            # print(incorrect, correct, mask1, mask2)
            success1  = int(mask2) != 0 and int(mask2) <= 1
            success5  = int(mask2) != 0 and int(mask2) <= 32
            success10 = int(mask2) != 0 and int(mask2) <= 1024
            results.append(((incorrect, correct), success1, success5, success10))
    result_data = {}
    for i in range(len(results)):
        # success_at_1, success_at_5, success_at_10 = success_at_k(results[i], tokens_pairs[i])
        # result_data[f'{tokens_pairs[i]}'] = {
        #     'success_at_1': success_at_1,
        #     'success_at_5': success_at_5,
        #     'success_at_10': success_at_10
        # }
        result_data[results[i][0]] = {
            'success_at_1':  1 if  results[i][1] else 0,
            'success_at_5':  1 if  results[i][2] else 0,
            'success_at_10': 1 if  results[i][3] else 0,
        }
    # print(json.dumps(result_data, indent=1))
    for measure in sorted(list(result_data[list(result_data.keys())[0]].keys())):
        print(measure, 'average:', round(pytrec_eval.compute_aggregated_measure(
                  measure, [query_measures[measure] for query_measures in result_data.values()]), 2))


if __name__ == '__main__':
    main()