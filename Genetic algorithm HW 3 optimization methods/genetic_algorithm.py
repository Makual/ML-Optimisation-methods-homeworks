from random import random, shuffle, sample
from base import Base
from path import Path


class GA(Base):

    def __init__(self, population: int, iter: int, s: float, m: float) -> None:
        """Initializes the hyperparameters for the algorithm."""
        self.population = population
        self.iter = iter
        self.s = s
        self.m = m

    def __fitness_sort(self, dm: list[list[float]], individuals: list[list[int]]) -> None:
        """Sorts the individuals of a given population by fit."""
        individuals.sort(key=lambda x: self._calculate_dist(dm,x))

    def __initialization(self, l: int) -> list[list[int]]:
        """Initializes the first population of individuals."""

        individuals = []
        for _ in range(self.population):
            perm = list(range(l))
            shuffle(perm)
            individuals.append(perm)

        return individuals

    def __selection(self, individuals: list[list[int]]):
        """Selects the best individuals of a given population."""

        return individuals[:int(self.population * self.s)]

    def __crossover(self, individuals: list[list[int]]):
        """Crossbreeding some individuals of a given population."""

        while len(individuals) < self.population:
            p1_idx, p2_idx = sample(range(len(individuals)), 2)
            parent1 = individuals[p1_idx]
            parent2 = individuals[p2_idx]

            l = len(parent1)

            i, j = sorted(sample(range(l), 2))

            child = [None] * l

            child[i:j] = parent1[i:j]

            pos = j
            for city in parent2:
                if city not in child:
                    if pos == l:
                        pos = 0
                    child[pos] = city
                    pos += 1

            individuals.append(child)

    def __mutation(self, individuals: list[list[int]]) -> None:
        """Mutates some individuals of a given population."""

        for i in range(1, len(individuals)):
            p1_idx, p2_idx = sample(range(len(individuals[0])), 2)

            if random() < self.m:
                individuals[i][p1_idx], individuals[i][p2_idx] = individuals[i][p2_idx], individuals[i][p1_idx]

    def run(self, points: list[tuple[int]], name: str = None) -> Path:
        """Runs the algorithm for the given 2D points."""

        dm = self._distance_matrix(points)
        individuals = self.__initialization(len(points))

        for _ in range(self.iter):
            self.__fitness_sort(dm, individuals)

            individuals = self.__selection(individuals)

            self.__crossover(individuals)
            self.__mutation(individuals)

        self.__fitness_sort(dm, individuals)

        return Path(individuals[0], self._calculate_dist(dm,individuals[0]), name)

if __name__ == "__main__":
    pass