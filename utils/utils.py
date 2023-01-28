import numpy as np
from nltk.corpus import wordnet


def min_edit_distance(token1, token2):
    dist_matrix = np.zeros((len(token1) + 1, len(token2) + 1))

    # initial values
    for i in range(len(token1) + 1):
        dist_matrix[i][0] = i
    for j in range(len(token2) + 1):
        dist_matrix[0][j] = j

    for i in range(1, len(token1) + 1):
        for j in range(1, len(token2) + 1):
            up_left = dist_matrix[i - 1][j - 1]
            if i == j and token1[i - 1] == token2[j - 1]:
                dist_matrix[i][j] = up_left
                continue
            up = dist_matrix[i - 1][j]
            left = dist_matrix[i][j - 1]
            dist_matrix[i][j] = min(up, left, up_left) + 1
    return int(dist_matrix[len(token1)][len(token2)])


def read_data(path):
    tokens = []
    with open(path, 'r') as f:
        lines = f.readlines()
        i = 0

        current_correct_token = ""
        for l in lines:
            if l.startswith("$"):
                current_correct_token = l[1:-1].lower()
            elif current_correct_token != "":
                tokens.append((current_correct_token, l[:-1].lower()))
            else:
                pass
    return tokens


def most_similar_words(token):
    similar_words = []
    dictionary = wordnet.words(lang='eng')
    for word in dictionary:
        med = min_edit_distance(token[1], word)
        if len(similar_words) < 10:
            similar_words.append((word, med))
        else:
            max_distance = max(similar_words, key=lambda a: a[1])
            if med < max_distance[1]:
                similar_words.remove(max_distance)
                similar_words.append((word, med))

    similar_words.sort(key=lambda a: (a[1], a[0]))
    return similar_words


def success_at_k(result, token_pair):
    s_at_1 = 0
    s_at_5 = 0
    s_at_10 = 0
    if token_pair[0] == result[0][0]:
        s_at_1 = 1
    if token_pair[0] in result[:5][0]:
        s_at_5 = 1
    if token_pair[0] in result[:][0]:
        s_at_10 = 1
    return s_at_1, s_at_5, s_at_10


# if __name__ == "__main__":
#     list_ = [('america', 1), ('american', 2), ('acerola', 3), ('ameba', 3), ('ameban', 3), ('amebic', 3),
#              ('amen-ra', 3),
#              ('amentia', 3), ('amerind', 3), ('average', 3)]
#     print(success_at_k(list_, ('america', 'amerkia')))
