import sys

import numpy as np

import matplotlib.pyplot as plt
from matplotlib import colors

from itertools import chain, combinations


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def summarize(arr):
    summary = []
    curr = 0
    for val in arr:
        if val == 1:
            curr += 1
        elif val == 0:
            if curr != 0:
                summary.append(curr)
                curr = 0
        else:  # val == -1
            assert False, 'Error: arr should only have 0 or 1'
    if curr != 0:
        summary.append(curr)
        curr = 0
    return summary


def update(state, axis, idx, true_summary):
    if axis == 'C':
        curr = state[:, idx]
    elif axis == 'R':
        curr = state[idx, :]
    else:
        assert False, 'Error: axis should be C or R'
    print(f'\nUpdating {axis}{idx}')
    print(f'Current value: {curr}')

    pos = np.where(curr == 1)[0]
    unknown = np.where(curr == -1)[0]

    if len(unknown) == 0:
        return False

    pset = powerset(unknown)

    variance = np.zeros(len(unknown), dtype=int)
    variants = 0
    for p in pset:
        test = np.zeros(len(curr), dtype=int)
        test[list(p)] = 1
        test[pos] = 1
        summary = summarize(test)
        if np.array_equal(summary, true_summary):
            variance += test[unknown]
            variants += 1

    print(f'Variance: {variance}')
    print(f'Variants: {variants}')

    if variants == 0:
        assert False, 'Error: no solution'

    new_pos = unknown[np.where(variance == variants)]
    new_neg = unknown[np.where(variance == 0)]

    if len(new_pos) + len(new_neg) == 0:
        return False

    curr[new_pos] = 1
    curr[new_neg] = 0
    print(f'New value: {curr}')
    return True


def validate(cols, rows):
    length = len(cols)
    assert length == len(rows), 'Error: length == len(rows) == len(cols)'
    for col in cols:
        assert sum(col) + len(col) - 1 <= length, f'Col Error: {col}'
    for row in rows:
        assert sum(row) + len(row) - 1 <= length, f'Row Error: {row}'
    print(length)


def extract(filename):
    cols = []
    rows = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        curr = 'NA'
        for line in lines:
            line = line[:-1]
            if curr == 'NA':
                assert line == 'C', 'Error: first line must be C'
                curr = 'C'
            elif curr == 'C':
                if line == 'R':
                    curr = 'R'
                else:
                    cols.append(list(map(int, line.split(' '))))
            elif curr == 'R':
                rows.append(list(map(int, line.split(' '))))

    print(cols)
    print(rows)

    validate(cols, rows)

    return cols, rows


def display(state, cols, rows):
    fig = plt.figure(figsize=(state.shape[0], state.shape[1]))
    ax = fig.add_subplot(1, 1, 1)

    ax.imshow(state, cmap=colors.ListedColormap(['white', 'white', 'black']))
    for i in range(state.shape[0]):
        for j in range(state.shape[1]):
            if state[i][j] == 0:
                ax.plot(j, i, marker='x', color='black', markersize=40)

    ax.set_xlim(-0.5, state.shape[0] - 0.5)
    ax.set_ylim(state.shape[1] - 0.5, -0.5)

    ax.set_xticks(minor=False, ticks=np.array(range(state.shape[0])) - 0.5)
    ax.set_yticks(minor=False, ticks=np.array(range(state.shape[1])) - 0.5)
    ax.set_xticks(minor=True, ticks=np.array(range(state.shape[0])),
                  labels=['\n'.join(map(str, col)) for col in cols])
    ax.set_yticks(minor=True, ticks=np.array(range(state.shape[1])),
                  labels=['  '.join(map(str, row)) for row in rows])

    ax.xaxis.tick_top()
    ax.tick_params(which='major', left=False, top=False,
                   labelleft=False, labeltop=False)
    ax.tick_params(which='minor', left=False, top=False,
                   labelleft=True, labeltop=True, labelsize=20)
    ax.grid()
    plt.savefig('nonogram.png')
    plt.close(fig)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python nonogram.py <filename>')
        sys.exit(1)

    filename = sys.argv[1]
    cols, rows = extract(filename)

    state = -np.ones((len(cols), len(rows)), dtype=int)

    change = True
    while change:
        change = False
        for i in range(len(cols)):
            change |= update(state, 'C', i, cols[i])

        for i in range(len(rows)):
            change |= update(state, 'R', i, rows[i])

        display(state, cols, rows)

    display(state, cols, rows)
