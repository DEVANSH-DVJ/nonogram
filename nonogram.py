import sys

import numpy as np

import matplotlib.pyplot as plt
from matplotlib import colors


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
            if state[i][j] == -1:
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


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python nonogram.py <filename>')
        sys.exit(1)

    filename = sys.argv[1]
    cols, rows = extract(filename)

    state = np.zeros((len(cols), len(rows)), dtype=int)
    # state = np.random.randint(-1, 2, size=(len(cols), len(rows)))

    print(state)
    display(state, cols, rows)
