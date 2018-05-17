import random

from jmetal.core.operator import Mutation
from jmetal.core.solution import BinarySolution, Solution, FloatSolution, IntegerSolution

""" Class implementing the binary BitFlip mutation operators """
__author__ = "Antonio J. Nebro"


class BitFlip(Mutation[BinarySolution]):
    def __init__(self, probability: float):
        super(BitFlip, self).__init__(probability=probability)

    def execute(self, solution: BinarySolution) -> BinarySolution:
        for i in range(solution.number_of_variables):
            for j in range(len(solution.variables[i])):
                rand = random.random()
                if rand <= self.probability:
                    solution.variables[i][j] = True if solution.variables[i][j] == False else False

        return solution


class Null(Mutation[Solution]):
    def __init__(self):
        super(Null, self).__init__(probability=0)

    def get_name(self):
        return "Null mutation"

    def execute(self, solution: Solution) -> Solution:
        return solution


class Polynomial(Mutation[FloatSolution]):
    def __init__(self, probability: float, distribution_index: float = 0.20):
        super(Polynomial, self).__init__(probability=probability)
        self.distribution_index = distribution_index

    def get_name(self):
        return "Polynomial mutation"

    def execute(self, solution: FloatSolution) -> FloatSolution:
        for i in range(solution.number_of_variables):
            rand = random.random()

            if rand <= self.probability:
                y = solution.variables[i]
                yl, yu = solution.lower_bound[i], solution.upper_bound[i]

                if yl == yu:
                    y = yl
                else:
                    delta1 = (y - yl) / (yu - yl)
                    delta2 = (yu - y) / (yu - yl)
                    rnd = random.random()
                    mut_pow = 1.0 / (self.distribution_index + 1.0)
                    if rnd <= 0.5:
                        xy = 1.0 - delta1
                        val = 2.0 * rnd + (1.0 - 2.0 * rnd) * (pow(xy, self.distribution_index + 1.0))
                        deltaq = pow(val, mut_pow) - 1.0
                    else:
                        xy = 1.0 - delta2
                        val = 2.0 * (1.0 - rnd) + 2.0 * (rnd - 0.5) * (pow(xy, self.distribution_index + 1.0));
                        deltaq = 1.0 - pow(val, mut_pow)

                    y += deltaq * (yu - yl)
                    if y < solution.lower_bound[i]:
                        y = solution.lower_bound[i]
                    if y > solution.upper_bound[i]:
                        y = solution.upper_bound[i]

                solution.variables[i] = y

        return solution


class IntegerPolynomial(Mutation[IntegerSolution]):
    def __init__(self, probability: float, distribution_index: float = 0.20):
        super(IntegerPolynomial, self).__init__(probability=probability)
        self.distribution_index = distribution_index

    def get_name(self):
        return "Polynomial mutation (Integer)"

    def execute(self, solution: IntegerSolution) -> IntegerSolution:
        for i in range(solution.number_of_variables):
            if random.random() <= self.probability:
                y = solution.variables[i]
                yl, yu = solution.lower_bound[i], solution.upper_bound[i]

                if yl == yu:
                    y = yl
                else:
                    delta1 = (y - yl) / (yu - yl)
                    delta2 = (yu - y) / (yu - yl)
                    mutPow = 1.0 / (self.distribution_index + 1.0)
                    rnd = random.random()
                    if rnd <= 0.5:
                        xy = 1.0 - delta1
                        val = 2.0 * rnd + (1.0 - 2.0 * rnd) * (xy ** (self.distribution_index + 1.0))
                        deltaq = val ** mutPow - 1.0
                    else:
                        xy = 1.0 - delta2
                        val = 2.0 * (1.0 - rnd) + 2.0 * (rnd - 0.5) * (xy ** (self.distribution_index + 1.0))
                        deltaq = 1.0 - val ** mutPow

                    y += deltaq * (yu - yl)
                    if y < solution.lower_bound[i]:
                        y = solution.lower_bound[i]
                    if y > solution.upper_bound[i]:
                        y = solution.upper_bound[i]

                solution.variables[i] = int(round(y))
        return solution


class SimpleRandom(Mutation[FloatSolution]):
    def __init__(self, probability: float):
        super(SimpleRandom, self).__init__(probability=probability)

    def get_name(self):
        return "Simple random mutation"

    def execute(self, solution: FloatSolution) -> FloatSolution:
        for i in range(solution.number_of_variables):
            rand = random.random()
            if rand <= self.probability:
                solution.variables[i] = solution.lower_bound[i] + \
                                        (solution.upper_bound[i] - solution.lower_bound[i]) * random.random()
        return solution


class Uniform(Mutation[FloatSolution]):
    def __init__(self, probability: float, perturbation: float = 0.5):
        super(Uniform, self).__init__(probability=probability)
        self.perturbation = perturbation

    def get_name(self):
        return "Uniform mutation"

    def execute(self, solution: FloatSolution) -> FloatSolution:
        for i in range(solution.number_of_variables):
            rand = random.random()

            if rand <= self.probability:
                tmp = (random.random() - 0.5) * self.perturbation
                tmp += solution.variables[i]

                if tmp < solution.lower_bound[i]:
                    tmp = solution.lower_bound[i]
                elif tmp > solution.upper_bound[i]:
                    tmp = solution.upper_bound[i]

                solution.variables[i] = tmp

        return solution
