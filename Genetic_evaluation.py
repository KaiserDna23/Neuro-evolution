#
# Class performing the evaluation of the algorithm
#

from Bird import Bird
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
            start, end, best_score, back_up = env(self.count, population_)
            # Set back population
            population_.set_population(back_up)
            #print(len(population_.get_population()))
            # Calculate fitness score, this will help in the creation of the next generation
            self.cal_fitness(population_.get_population())
            # get the best fitness score
            best_fitness = population_.get_best_fitness()

            # print and save information
            self.report(start, end, best_score, best_fitness)

            # Next step create mating pool and produce the next generation
            next_gen_list = self.matting_pool(population_.get_population())
            print(next_gen_list)
            next_gen = population_.set_population(next_gen_list)

            print('\n ')
            print('+'*90)
            print('> NEXT GENERATION CREATED\n ')


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
        messages = [f"ID   |  start_time(s)  |  End_time(s)  |  Time spent(s)  |   Best score   |   Best fitness",
                    f"{self.count}    |   {round(time_s,2)}      |   {round(time_e,2)}     |   {round(time_e - time_s)}         |      {best_score}      |  {best_fitness}"]

        print("*" * 90)
        print(messages[0])
        print(messages[1])

        # Store inside file
        with open('evolution_txt.txt', '+a') as file:
            for message in messages:
                file.write(message)
                file.write("\n")
        file.close()

        # Matting pool

    def matting_pool(self, population):
        """
        Perform matting on population individuals.
        Choose the best 2 and make them share their weights with the rest of the population.

        :return: new_population,  a list containing the new generation
        """
        new_population = []
        chosen_one = self.__selection__(population)
        # Use most fitted instances to reproduce with
        if len(population) >= 1:
            for element in population:
                if chosen_one is not element:
                    x_, y_ = self.population.__rand_position__()
                    new_population.append(Bird(x_, y_, parents=[chosen_one, element]).mutation(0.1))

            # add the parent to the generation
            new_population.append(chosen_one)

            return new_population

    def cal_fitness(self, population):
        """
        Calculate and assign fitness based on score of individuals, the fitness is calculated as follows:
        fit = score/sum_score.
        This ensures that every value will be < 1, and so doing, represents each bird probability of being chosen.
        """
        sum_ = 0
        sorted_ = {}
        # Get the sum of all scores
        for i in range(0, len(population)):
            sum_ += population[i].get_score()

        for i in range(0, len(population)):
            if population[i].get_score() <= 0 or sum_ <= 0:
                fitness = 0
                population[i].set_fitness(fitness)
                sorted_.update({str(fitness): population[i]})

            else:
                fitness = population[i].get_score() / sum_
                population[i].set_fitness(int(fitness))
                sorted_.update({str(fitness): population[i]})

        # print(population)
        # print(sorted_)
        # print(sorted_.keys())
        self.population.set_highestFitness(sorted(list(sorted_.keys()))[0])

    def __selection__(self, population):
        """
        Select the best couple of individuals performing well.
        :return: chosen_ones, a couple of individuals
        """
        scores_ = {}

        if len(population) >= 1:
            # Relate score to individual, then sort by score
            for i in range(0, len(population)):
                scores_.update({str(population[i].get_fitness()): population[i]})

            # Sort the keys(fitness score) in reverse order and then return the highest
            keys = sorted(list(scores_.keys()), reverse=True)
            # With keys sorted the best/ highest is located at first position
            key = keys[0]
            self.population.best_score = scores_[key].get_score()
            return scores_[key]
