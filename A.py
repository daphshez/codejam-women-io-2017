"""
Problem

A group of F friends is attending a conference held at an amphitheater, and they have bought tickets to see a concert
there afterwards. The amphitheater is a grid of seats with S rows and S columns. For each seat, the amphitheater has
sold a single ticket (although some of the tickets might not have been sold to this group of friends). Each ticket is
normally labeled with a pair of integers giving the row and column numbers of one seat, in that order. For example, a
ticket might normally say (2, 1), meaning row 2, column 1, or (2, 2), meaning row 2, column 2.

When the tickets were printed, there was a malfunction, and the two numbers in each pair always came out in sorted
(that is, nondecreasing) order! So, for example, a ticket labeled (1, 2) might actually be for the seat in row 1,
column 2, or it might actually be for the seat in row 2, column 1. If two friends have tickets labeled (1, 2), then one
must actually be for row 1, column 2, and the other must actually be for row 2, column 1.

The friends will consult the box office on the day of the concert to find out what their actual seat numbers are, but
for now, it is unclear! Given the printed pairs on the tickets, what is the largest possible number of the friends that
 could actually be seated all in the same-numbered row of seats? (The friends do not necessarily need to be seated in
  consecutive seats in that row.)

Input

The first line of the input gives the number of test cases, T. T test cases follow. Each begins with one line with two
integers F and S, representing the number of friends and the dimension of the grid of seats. Then, F more lines follow.
The i-th of those lines has two integers Ai and Bi, representing the two numbers printed on the i-th friend's ticket.

Output

For each test case, output one line containing Case #x: y, where x is the test case number (starting from 1) and y i
 largest possible number of the friends that could actually be seated all in the same-numbered row of seats.

Limits

F ≤ S2.
1 ≤ Ai ≤ Bi ≤ S, for all i.
No pair appears more than twice in a test case.
No pair containing the same number twice appears more than once in a test case.
Small dataset

1 ≤ T ≤ 50.
2 ≤ F ≤ 3.
2 ≤ S ≤ 3.
Large dataset

1 ≤ T ≤ 100.
2 ≤ F ≤ 100.
2 ≤ S ≤ 100.
Sample


"""

from collections import Counter

from CodeJam import CodeJamProblem


class A(CodeJamProblem):
    def __init__(self):
        super().__init__('A')

    def generate_test_cases(self, input_file):
        with open(input_file) as fin:
            cases = int(next(fin).strip())
            for _ in range(cases):
                (f, s) = [int(x) for x in next(fin).strip().split(' ')]
                lines = [next(fin).strip().split(' ') for _ in range(f)]
                yield f, s, (tuple(t) for t in lines)

    def solve(self, t):
        f, s, tickets = t
        ticket_set = set()
        c = Counter()
        for ticket in tickets:
            if ticket[0] == ticket[1]:
                c[ticket[0]] += 1
            elif ticket in ticket_set:
                pass
            else:
                c[ticket[0]] += 1
                c[ticket[1]] += 1
            ticket_set.add(ticket)
        return min(f, max(c.values()), s)



a = A()
a.test()
