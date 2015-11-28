# coding=utf-8

import random

Inf = float("inf")


class Chromosome:
    def __init__(self, conf, init_genome=True):
        self.conf = conf
        self.fitness = 0.0
        self.d = Inf
        if init_genome:
            self.genome = [random.randint(0, self.conf['nodes_count'] - 1) for _ in xrange(self.conf['genome_size'])]
            self.genome[0] = self.conf["start_node"]
            self.genome[-1] = self.conf["finish_node"]
            self.eval_fitness()
        else:
            self.genome = []

    def mutate(self):
        if len(self.genome) > 2:
            c1 = random.randint(1, len(self.genome)-2)
            self.genome[c1] = random.randint(0, self.conf['nodes_count'] - 1)

    @classmethod
    def crossover(cls, ch1, ch2):
        ch = Chromosome(ch1.conf, False)
        ch.genome = ch1.genome[:len(ch1.genome)/2] + ch2.genome[len(ch2.genome)/2:]
        return ch

    def eval_fitness(self):
        self.d = 0.0
        for i in xrange(0, len(self.genome) - 1):
            gene_a = self.genome[i]
            gene_b = self.genome[i + 1]

            self.d += self.conf['graph'][gene_a][gene_b]

        try:
            self.fitness = 1.0/self.d
        except ZeroDivisionError:
            self.fitness = Inf
        return self.fitness

    def __unicode__(self):
        return "[ " + " ".join(self.genome) + " ]"

    def __str__(self):
        return "[ " + " ".join(map(lambda x: str(x), self.genome)) + " ]"


class GeneticAlgorithm:
    DEFAULT_CONFIG = {
        'graph': None,
        'population_size': 10,
        'mutation_prob': 0.2,
        'selection_count': 5,
        'genome_size': 1,
        'start_node': 1,
        'finish_node': 1
    }

    def __init__(self):
        self.conf = {}
        self.population = []

    def clear(self):
        self.conf = {}
        self.population = []

    def init_config(self,conf):
        self.clear()
        self.conf = self._init_config(conf)
        self.population = [Chromosome(self.conf) for _ in xrange(self.conf['population_size'])]

    def _init_config(self, conf):
        if 'start_node' not in conf:
            raise Exception("Start node not supplied")
        if 'finish_node' not in conf:
            raise Exception("Finish node not supplied")
        if 'graph' not in conf:
            raise Exception("Graph not supplied")
        conf['nodes_count'] = len(conf['graph'])
        for (k, v) in self.DEFAULT_CONFIG.iteritems():
            if k not in conf:
                conf[k] = v
        return conf

    def step(self): #мутация,скрещивание
        p1 = random.choice(self.population[:self.conf['selection_count']])
        p2 = random.choice(self.population[:self.conf['selection_count']])

        child = Chromosome.crossover(p1, p2)

        if random.random() < self.conf['mutation_prob']:
            child.mutate()

        child.eval_fitness()

        self.population.append(child)

        self.population = sorted(self.population, key=lambda x: x.fitness, reverse=True)
        self.population = self.population[:self.conf['population_size']]

    def get_state(self):
        # return self.population, self.other_userful_stuff ... (возвращаем состояние которе нужно юзеру)
        return self.population


if __name__ == "__main__":
    ga = GeneticAlgorithm()
    graph = [
        [0, 2, 1, Inf, 10],
        [2, 0, 4, 3, 1],
        [1, 4, 0, 1, Inf],
        [Inf, 3, 1, 0, 1],
        [10, 1, Inf, 1, 0],
    ]
    conf = {
        'graph': graph,
        'population_size': 8,
        'mutation_prob': 0.2,
        'selection_count': 5,
        'genome_size': len(graph),
        'start_node': 0,
        'finish_node': 4
    }

    ga.init_config(conf)

    for _ in xrange(100):
        ga.step()

    for ch in ga.population:
        print(str(ch), ch.fitness, ch.d)
    pass
