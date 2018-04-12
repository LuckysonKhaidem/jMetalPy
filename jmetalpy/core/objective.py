from jmetalpy.core.problem import Problem
from jmetalpy.core.solution import Solution

__author__ = "Antonio J. Nebro"


class Objective:
    def compute(self, solution: Solution, problem: Problem) -> float:
        pass

    def is_a_minimization_objective(self) -> bool:
        return True
