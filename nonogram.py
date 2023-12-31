import sys

import numpy as np

import matplotlib.pyplot as plt
from matplotlib import colors

from itertools import chain, combinations


# Helper functions related to initialize nonogram state #

def init(filename):
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

    for col in cols:
        assert sum(col) + len(col) - 1 <= len(rows), f'Col Error: {col}'
    for row in rows:
        assert sum(row) + len(row) - 1 <= len(cols), f'Row Error: {row}'

    state = -np.ones((len(rows), len(cols)), dtype=int)

    print(cols)
    print(rows)
    print(state.shape)

    return cols, rows, state


# Helper functions related to updating nonogram state #

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
    print(f'True summary: {true_summary}')

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


# Helper functions related to display nonogram state #

def add_lines(ax, shape):
    for i in range(0, shape[1] + 1, 5):
        ax.plot([i - 0.5, i - 0.5], [-0.5, shape[0] - 0.5],
                color='blue', linewidth=5)

    for i in range(0, shape[0] + 1, 5):
        ax.plot([-0.5, shape[1] - 0.5], [i - 0.5, i - 0.5],
                color='blue', linewidth=5)


def display(state, cols, rows):
    fig = plt.figure(figsize=(state.shape[1], state.shape[0]))
    ax = fig.add_subplot(1, 1, 1)

    ax.imshow(state, cmap=colors.ListedColormap(['white', 'white', 'black']))
    for i in range(state.shape[0]):
        for j in range(state.shape[1]):
            if state[i][j] == 0:
                ax.plot(j, i, marker='x', color='black', markersize=40)

    add_lines(ax, state.shape)

    ax.set_xlim(-0.5, state.shape[1] - 0.5)
    ax.set_ylim(state.shape[0] - 0.5, -0.5)

    ax.set_xticks(minor=False, ticks=np.array(range(state.shape[1])) - 0.5)
    ax.set_yticks(minor=False, ticks=np.array(range(state.shape[0])) - 0.5)
    ax.set_xticks(minor=True, ticks=np.array(range(state.shape[1])),
                  labels=['\n'.join(map(str, col)) for col in cols])
    ax.set_yticks(minor=True, ticks=np.array(range(state.shape[0])),
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
    cols, rows, state = init(filename)
    display(state, cols, rows)

    change = True
    while change:
        change = False
        for i in range(len(cols)):
            change |= update(state, 'C', i, cols[i])

        for i in range(len(rows)):
            change |= update(state, 'R', i, rows[i])

        display(state, cols, rows)

    display(state, cols, rows)

    print('\nSolved!')
