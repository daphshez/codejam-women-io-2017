"""
Problem

In honor of Google I/O 2017, we would like to make an I/O-themed word search grid. This will be a rectangular grid in
which every cell contains one of the three characters I, /, or O. The people solving our word search will look for all
instances of the string I/O that appear contiguously forwards or backwards in a row, column, or diagonal. For example,
the following grid contains eight instances of I/O, representing all eight possible directions in which the string can
appear:

OOOOO
O///O
O/I/O
O///O
OOOOO
To control the difficulty level of our word search, we would like the string to appear exactly N times in the grid.
Moreover, we do not want the grid to be too large; it cannot have more than D rows or more than D columns.

Can you help us design a grid that meets these specifications?

Input

The first line of the input gives the number of test cases, T. T test cases follow. Each test case consists of one line
with two integers D and N, as described above.

Output

For each test case, first output one line containing Case #x:. Then output R lines of exactly C characters each,
representing the rectangular grid. Each of those characters must be either I, /, or O. You may choose any values of
R and C as long as both are at least 1 and neither exceeds D. Your grid must contain exactly N instances of the string
I/O, per the rules described in the statement.

If there are multiple valid answers, you may output any of them.

Limits

0 ≤ N ≤ 287.
It is guaranteed that at least one valid grid exists for each test case.

Small dataset
1 ≤ T ≤ 25.
D = 50.

Large dataset
1 ≤ T ≤ 100.
D = 15.
"""

# this code should work but it produces a matrix of exactly size DxD, where the problem allows for a smaller one

from CodeJam import *

pattern_str = """ABCBA
B*B*B
CBABC
B*B*B
ABCBA
"""
pattern = [[x for x in line] for line in pattern_str.split("\n")]


def char_at_location(i, j):
    return pattern[i % 4][j % 4]


def word_search(d, n):
    if d <= 2:
        return None
    base_d = d if (d % 2) == 1 else d - 1
    base = [[char_at_location(i, j) for i in range(base_d)] for j in range(base_d)]
    if d % 2 == 0:
        for i, line in enumerate(base):
            line.append(pattern[i % 4][0])
        base.append([pattern[0][j % 4] for j in range(d - 1)] + ["*"])
    lines = "\n".join("".join(line) for line in base)
    count = lines.count("B")
    while count < n:
        return None
    return lines.replace('B', '*', count - n)


def translate_to_io(s):
    return s.translate(bytes.maketrans(b"ABC*", b"I/OO"))


class C(CodeJamProblem):
    def __init__(self, name):
        super().__init__(name, result_formatter=lambda s: "\n%s" % s)

    def test(self):
        pass

    def generate_test_cases(self, input_file):
        with open(input_file) as f:
            for _ in range (int(next(f).strip())):
                yield tuple(int(x) for x in next(f).strip().split(' '))

    def solve(self, t):
        d, n = t
        return translate_to_io(word_search(d, n))

