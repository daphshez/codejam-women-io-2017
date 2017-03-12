input_folder = 'data'


def float_formatter(f):
    return "%.06f" % f


class CodeJamProblem:
    def __init__(self, name, result_formatter=lambda x: '%s' % x):
        self.name = name
        self.result_formatter = result_formatter

    # override this!
    def generate_test_cases(self, input_file):
        return []

    # override this!
    def solve(self, t):
        return 0

    def input_file(self, stage):
        return '%s/%s-%s.in' % (input_folder, self.name, stage)

    def output_file(self, stage):
        return '%s/%s-%s.out' % (input_folder, self.name, stage)

    def run(self, input_file, output_file):
        with open(output_file, 'w') as f:
            for i, t in enumerate(self.generate_test_cases(input_file)):
                f.write("Case #%d: %s\n" % (i + 1, self.result_formatter(self.solve(t))))

    def test(self):
        self.stage('test')
        expected = open("data/%s-test-expected.out" % self.name).read().strip()
        actual = open(self.output_file('test')).read().strip()
        if expected == actual:
            print("Test successful!")
        else:
            print("Test failed!")
            print(actual)

    def stage(self, stage):
        self.run(self.input_file(stage), self.output_file(stage))

    def small(self, attempt):
        self.stage('attempt%s' % attempt)

    def large(self):
        self.stage('large')
