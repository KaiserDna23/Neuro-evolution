#
# Class performing the evaluation of the algorithm
#

from Population import Population


class GeneticEvaluation:
    """
    Class describing the eval simple evaluation of each generation of the population
    """
    def __init__(self, population: Population, max_generation: int):
        """
        :param population: Population instance containing initialized elements.
        :param max_generation: Integer, representing the maximum number of generation allowed
        """

        self.count = 0
        self.max_generation = max_generation
        self.population = population

    def run(self, env):
        """
        Run the population through the fitness function until max generation reaches

        :param env: Represent the environment to which we will submit the individuals
        :return: Element with the highest fitness score
        """
        population_ = self.population
        if callable(env):
            for i in range(self.max_generation):
                population_ = self.run_generation(env, population_)

    def run_generation(self, env, population: Population):
        """
        Run an instance of population until it get extinct.

        :param env: Represent the environment to which we will submit the individuals
        :param population: List of objects representing the population
        """

        # Check if we have exceeded the limit of generations
        if self.count <= self.max_generation:
            population_ = population
            # increase generation count
            self.count += 1
            # run the environment
            start, end, best_score = env(population_)
            # Calculate fitness score, this will help in the creation of the next generation
            population_.cal_fitness()
            # get the best fitness score
            best_fitness = population_.get_best_fitness()

            # print and save information
            self.report(start, end, best_score, best_fitness)

            # Next step create mating pool and produce the next generation
            next_gen_list = population_.matting_pool()
            next_gen = population_.set_population(population)

            # replace the old population
            population_ = next_gen

            return population_

    def next_generation(self, population):
        """
        Create the next generation by choosing element with high fitness score to reproduce.

        :param population: List containing the population.
        :return next_generation: List containing the new generation
        """

    def report(self, time_s, time_e, best_score, best_fitness):
        """
        Report present the different information about a generation, this includes,
        the start time, end time, best score, the highest fitness score.
        All information presented shall be recorded inside a file.

        :param time_s: Start time of generation.
        :param time_e: End time of generation.
        :param best_score: The best score performed by generation.
        :param best_fitness: The best fitness score performed by generation
        """
        messages = [f"ID  |  start_time  | End_time  |  Time spent  |  Best score  |  Best fitness",
                    f"{self.count}  |  {time_s}  |  {time_e}  |  {round(time_e - time_s)}  |   {best_score}  |  {best_fitness}"]

        print("*" * 12)
        print(messages[0])
        print(messages[1])

        # Store inside file
        with open('evolution_txt.txt', '+a') as file:
            for message in messages:
                file.write(message)

            file.close()
