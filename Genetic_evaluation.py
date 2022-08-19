#
# Class performing the evaluation of the algorithm
#

class GeneticEvaluation:

    def __int__(self, population, max_generation):
        self.max_generation = population
        self.population = max_generation

    def run(self, env):
        """
        Run the population through the fitness function until max generation reaches

        :param env: Represent the environment to which we will submit the individuals
        :return: Element with the highest fitness score
        """
        count = 0
        if callable(env):
            env = env(self.population.get_population())

    def run_generation(self, env, count, population):
        """
        Run an instance of population until there's no one left.

        :param env: Represent the environment to which we will submit the individuals
        :param population: List of objects representing the population
        :param count: Integer representing the actual generation
        """
        time_out = False if count < self.max_generation else True
        while time_out is False and population.extinct is False:
            # increasing generation count
            count += 1
            env_ = env(population)






    def next_generation(self, population):
        """
        Create the next generation by choosing element with high fitness score to reproduce.

        :param population: List containing the population.
        :return next_generation: List containing the new generation
        """



    def report(self):
        pass