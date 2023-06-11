import sys


def validate(cols, rows):
    length = len(cols)
    assert length == len(rows), "Error: length == len(rows) == len(cols)"
    for col in cols:
        assert sum(col) <= length, "Error: sum(col) <= length"
    for row in rows:
        assert sum(row) <= length, "Error: sum(row) <= length"
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
                assert line == 'C', "Error: first line must be 'C'"
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


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python nonogram.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    cols, rows = extract(filename)
