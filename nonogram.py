import sys


def extract(filename):
    col = []
    row = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        curr = 'NA'
        for line in lines:
            line = line[:-1]
            if curr == 'NA':
                if line == 'C':
                    curr = 'C'
                else:
                    print("Error: first line must be 'C'")
            elif curr == 'C':
                if line == 'R':
                    curr = 'R'
                else:
                    col.append(list(map(int, line.split(' '))))
            elif curr == 'R':
                row.append(list(map(int, line.split(' '))))

    print(col)
    print(row)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python nonogram.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    extract(filename)
