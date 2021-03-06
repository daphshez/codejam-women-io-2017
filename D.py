"""
Problem D. Where Ya Gonna Call?

Gooli is a huge company that owns B buildings in a hilly area. The buildings are numbered from 1 to B.

Last year, they built a set of slides between buildings that are now the favorite form of transportation between
buildings. Slides have been upgraded with suction technology to make them two-way, so a slide between two buildings can
be used to travel between those buildings in either direction. Some slides were built with turns, so their lengths do
not necessarily follow common sense; for instance, they do not necessarily comply with the triangle inequality. Also,
 there is at most one slide between any pair of buildings.

Gooli is going to choose a location to install a special super secure phone for the CEO to talk to other important
people. They want to minimize the distance by slide from any building to the meeting location, so as to minimize the
time that it would take the CEO to reach it from any building. Gooli does not have any more carbon kilotubes to build
more slides, and the CEO refuses any other type of transportation, so Gooli's communication security team needs to find
the best location that is reachable using only already existing slides. The location could be in a building or a point
somewhere within a slide.

When traveling using the slides, the CEO may use a slide, arrive at a building, then use a slide that starts there,
arrive at another building, and so on, until she arrives at the desired location. Slides used from end to end contribute
their full length to the total distance. If the CEO enters a slide and stops inside it because she found the phone, on
the other hand, only the used part of the slide contributes to the total distance. When measuring distance, only the
slide distance is important. Distance traveled within buildings to connect to a new slide or reach the phone is
considered to be zero.

Given the buildings and slides in existence, can you find any optimal location for the super secure phone and return the
distance from a farthest building to it? Note that the distance is the same for any optimal location.

Input

The first line of the input gives the number of test cases, T. T lines follow. Each test case starts with one line with
a single integer B, the number of buildings on Gooli's campus. Then, B - 1 lines follow. For i = 2, 3, ..., B, the
(i-1)-th of these lines contains (i-1) integers Di1, Di2, ..., Di(i-1). Dij is -1 if there is no slide between the i-th
building and the j-th building, or the length of that slide otherwise. All buildings are reachable from any other
building using only slides, possibly passing through intermediate buildings.

Output

For each test case, output one line containing Case #x: y, where x is the test case number (starting from 1) and y is
the distance from an optimal location for the phone to a building farthest from it. y will be considered correct if it
is within an absolute or relative error of 10-6 of the correct answer. See the FAQ for an explanation of what that
means, and what formats of real numbers we accept.

Limits

1 ≤ T ≤ 100.
2 ≤ B ≤ 50.
All buildings are reachable from any other building using only slides, possibly passing through intermediate buildings.
Dij ≠ 0, for all i, j.
Small dataset

-1 ≤ Dij ≤ 2, for all i, j.
Large dataset

-1 ≤ Dij ≤ 109, for all i, j.
Sample

"""

from CodeJam import *


# All Pairs Shortest Path Implementation
# https://github.com/heineman/python-algorithms/blob/master/7.%20Seven%20All%20Pairs%20Shortest%20Path/apsp.py
def allPairsShortestPath(g):
    """Return distance structure as computed"""
    dist = {}
    pred = {}
    for u in g:
        dist[u] = {}
        pred[u] = {}
        for v in g:
            dist[u][v] = 999999999999999999
            pred[u][v] = None

        dist[u][u] = 0
        pred[u][u] = None

        for v in g[u]:
            dist[u][v] = g[u][v]
            pred[u][v] = u

    for mid in g:
        for u in g:
            for v in g:
                newlen = dist[u][mid] + dist[mid][v]
                if newlen < dist[u][v]:
                    dist[u][v] = newlen
                    pred[u][v] = pred[mid][v]

    return dist, pred


def find_first_neighbor_in_path(prev):
    # fix the ones directly adjacent to the source, to point to themselves rather than to the source
    for u in prev:
        for v in prev[u]:
            if prev[u][v] == u:
                prev[u][v] = v
    # now the actual back tracking
    for _ in range(len(prev)):
        for u in prev:
            for v in prev[u]:
                p = prev[u][v]
                if p is not None and prev[u][p] != u:
                    prev[u][v] = prev[u][p]
    return prev


def build_graph(lines):
    graph = {i: {} for i in range(len(lines) + 1)}
    for i, line in enumerate(lines):
        for j, d in enumerate(int(x) for x in line.strip().split(" ")):
            if d != -1:
                graph[i + 1][j] = d
                graph[j][i + 1] = d
    return graph


def improve_max(distances, first_steps, a):
    """
    a is the proposed centre. See if we can improved the max distance by locating the phone on an edge that leaves it.
    :param distances: distance matrix d[u][v] is the distance from u to v
    :param first_steps: d[u][v] the first vertex on the optimal route from u to v (u excluded)
    :param a: suggested centre
    :return: optimal maximum trip size if it's on an edge adjacent to a
    """

    def check_edge_to(b):
        """
        :param b: vertex, neighbour of a
        :return: the maximum distance if it's on the edge between a and b
        """
        # vertices that are closer to a than to b
        friends_of_a = [v for v in distances[a] if distances[a][v] <= distances[b][v]]
        # maximum distance between a and any of its friends
        m_a = max(distances[a][v] for v in friends_of_a)
        # now the same of alternative centre
        friends_of_b = [v for v in distances[a] if distances[a][v] >= distances[b][v]]
        m_b = max(distances[b][v] for v in friends_of_b)

        # check special case - exists v s.t. d(a, v) == d(b, v) == m_a  == m_b)
        if m_a == m_b:
            friends_at_max_distance_of_a = set(v for v in friends_of_a if distances[a][v] == m_a)
            friends_at_max_distance_of_b = set(v for v in friends_of_b if distances[b][v] == m_b)
            if len(friends_at_max_distance_of_a.intersection(friends_at_max_distance_of_b)) > 0:
                return max_distance     # this is max_distance of any node from a, calculated by the wrapping function

        if m_a >= m_b + distances[a][b]:
            return m_a
        elif m_b >= m_a + distances[a][b]:
            return m_b
        else:
            return m_a + (distances[a][b] + m_b - m_a) / 2

    # find the maximum distance that needs to be travelled from anywhere to suggested_centre
    max_distance = max(distances[a][v] for v in distances[a])
    # find all furthermost nodes - all nodes that are at maximum_distance distance from suggested_centre
    possible_furthermost = [v for v in distances[a] if distances[a][v] == max_distance]
    # find how much we can improve max_distance for each c we pick; look for the best improvement
    return max(check_edge_to(first_steps[a][v]) for v in possible_furthermost)


class D(CodeJamProblem):
    def __init__(self):
        super().__init__('D', float_formatter)

    def generate_test_cases(self, input_file):
        with open(input_file) as f:
            cases = int(next(f).strip())
            for _ in range(cases):
                b = int(next(f).strip())
                yield build_graph([f.readline() for _ in range(b - 1)])

    def solve(self, graph):
        if len(graph) < 2:
            return 0
        if len(graph) == 2:
            return graph[0][1] / 2
        if max(graph[u][v] for u in graph for v in graph[u]) == 0:
            return 0

        distances, parents = allPairsShortestPath(graph)
        first_steps = find_first_neighbor_in_path(parents)
        # for each u, find the distance to the furthermost node from it; keep the mode u and the distance
        max_dist_from_u = [(u, max(distances[u][v] for v in distances[u])) for u in distances]
        # keep only the vertices with the minimum maximum distance
        min_max_distance = min(t[1] for t in max_dist_from_u)
        # find the vertices with the minimal maximum distance
        possible_centres = [t[0] for t in max_dist_from_u if t[1] == min_max_distance]
        # try to improve the maximum distance on the possible centres
        improved_maxes = [improve_max(distances, first_steps, t) for t in possible_centres]
        return min(improved_maxes)


d = D()
d.test()
