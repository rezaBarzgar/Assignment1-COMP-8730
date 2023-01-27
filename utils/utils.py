import csv

import numpy as np


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
    print(np.array_str(dist_matrix, precision=2))


def write_csv(name, data):
    with open(f'{name}.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile)
        writer.writeheader()
        writer.writerows(data)


def cal_med(path):
    file = open(path, 'r')
    lines = file.readlines()
    words = {}
    correct_word = ''
    for line in lines:
        token = line[:-1].lower()
        if '$' in line:
            correct_word = token
            words[correct_word] = list()
        else:
            words[correct_word].append(token)


if __name__ == "__main__":
    cal_med('..\data\missp.dat')
