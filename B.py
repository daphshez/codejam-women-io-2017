"""
Problem

You are a casting director for an upcoming musical. The musical has N roles, and for each role, you want to cast two
performers: one primary performer and one understudy. A primary performer or understudy trains for only one particular
role, and the job of the understudy is to play the role if the primary performer becomes unavailable. At least one of
the two performers for each role must be available for the show to succeed.

You have selected 2N performers to be in the musical. They are all quite talented, and any of them can be cast as a
primary performer or understudy for any of the roles. However, you are worried that some of them may be tempted to run
away to join the cast of Hamiltonian!, the smash hit musical about quantum mechanics, before your show opens. Luckily,
you are an excellent judge of character. You know that the i-th performer has a probability Pi of becoming unavailable.
(These probabilities are all independent of each other, and a given performer has their probability regardless of their
assigned role or whether they are a primary performer or understudy.)

You wish to assign one primary performer and one understudy for each role in a way that maximizes the probability that
the show will succeed. That is, you want to minimize the probability that there will be at least one role for which the
primary performer and understudy both become unavailable.

If you make optimal casting choices, what is the probability that your show will succeed?

Input

The first line of the input gives the number of test cases, T. T test cases follow; each consists of two lines. The
 first line contains a single integer N: the number of roles. The second line contains 2N rational numbers Pi; the i-th
 of these gives the probability that the i-th performer will become unavailable for your show. All of these
 probabilities are specified to exactly four decimal places of precision.

Output

For each test case, output one line containing Case #x: y, where x is the test case number (starting from 1) and y is
the probability that your show will succeed. y will be considered correct if it is within an absolute or relative error
of 10-6 of the correct answer. See the FAQ for an explanation of what that means, and what formats of real numbers we
accept.

Limits

1 ≤ T ≤ 100.
0.0000 ≤ Pi ≤ 1.0000, for all i.

Small dataset
1 ≤ N ≤ 4.

Large dataset
1 ≤ N ≤ 40.
"""

from functools import reduce
from operator import mul
from CodeJam import *


class B(CodeJamProblem):
    def __init__(self):
        super().__init__('B', float_formatter)

    def solve(self, t):
        assert len(t) % 2 == 0, t
        n_roles = len(t) // 2
        sorted_probabilities = list(sorted(t))
        first_half = sorted_probabilities[:n_roles]
        second_half = reversed(sorted_probabilities[n_roles:])
        role_success_probabilities = (1 - p1 * p2 for (p1, p2) in zip(first_half, second_half))
        return reduce(mul, role_success_probabilities, 1)

    def generate_test_cases(self, input_file):
        with open(input_file) as f:
            t = int(next(f))
            for _ in range(t):
                next(f)
                yield [float(x) for x in f.readline().strip().split(' ')]

b = B()
b.test()
b.stage('small-practice')
b.stage('large-practice')

