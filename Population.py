# Population class

from random import randint
from Bird import Bird
from multiprocessing import Process, Pool

class Population:
    width_screen = 576
    height_screen = 800

    def __init__(self, nber_individuals:int):
        self.population = []
        self.extinct = False
        self.generations_scores = {}
        self.best = 0
        self.__generate_population__(nber_individuals)

    #################################################################
    ################## Class Methods
    ################################################################

    # get population
    def get_population(self):
        return self.population

    # get the best score
    def get_best(self):
        return self.best

    # get extinct
    def get_exinct(self):
        return self.extinct

    # set the extinction alarm
    def set_extinct(self):
        self.extinct = True

    # get individual
    def get_element(self, index):
        """
        Get an element by its position
        :param index: integer representing the position of an element
        :return:
        """
        return self.population[index]

    # random position generator
    def __rand_position__(self):
        rand_x = randint(0, int(self.width_screen / 4))
        rand_y = randint(0, int(self.height_screen / 4))
        return rand_x, rand_y

    # generate population
    def __generate_population__(self, nber_individuals):
        """
        Initialise the population, i.e, populate, create instances of bird class.

        :param nber_individuals: Represents the total number of individuals in the population.
        """
        for i in range(nber_individuals):
            x_, y_ = self.__rand_position__()
            self.population.append(Bird(x_, y_))

        self.best = self.population[0]


    def cal_fitness(self):
        """
        Calculate and assign fitness based on score of individuals, the fitness is calculated as follows:
        fit = score/sum_score.
        This ensures that every value will be < 1, and so doing, represents each bird probability of being chosen.
        """
        sum_ = 0
        # Get the sum of all scores
        for i in range(0, len(self.population)-1):
            sum_ += self.population[i].get_score()

        for i in range(0, len(self.population)-1):
            if self.population[i].get_score() <= 0 or sum == 0:
                fitness = 0
            else:
                fitness = self.population[i].get_score()/sum_
            self.population[i].set_fitness(fitness)


    def __selection__(self):
        """
        Select the best couple of individuals performing well.
        :return: chosen_ones, a couple of individuals
        """
        scores_ = {}
        sorted_population = []

        if len(self.population) >= 1:
            # Relate score to individual, then sort by score
            for i in range(0, len(self.population) - 1):
                scores_.update({self.population[i].get_fitness(): self.population[i]})


            # Sort the keys in reverse order and then return the highest 4
            keys = sorted(scores_.keys(), reverse=True)
            if len(keys) >= 1:
                for key in keys[:2]:
                    sorted_population.append(scores_[key])
                # Get and set the best score in generation
                #self.best = sorted_population[0].get_score()
                return [sorted_population[0], sorted_population[1]]
            else:
                sorted_population.append(scores_[keys[0]])
                # Get and set the best score in generation
                #self.best = sorted_population[0].get_score()
                return [sorted_population[0]]



    # Matting pool
    def matting_pool(self):
        """
        Perform matting on population individuals.
        Choose the best 2 and make them share their weights with the rest of the population.

        :return: new_population,  a list containing the new generation
        """
        new_population = []
        chosen_ones = self.__selection__()
        # Use most fitted instances to reproduce with
        if len(self.population) >= 1 and len(chosen_ones) >= 1:
            for instance in chosen_ones:
                if instance not in self.population:
                    for element in self.population:
                        x_, y_ = self.__rand_position__()
                        new_population.append(Bird(x_, y_, parents=[instance, element]).mutation(0.1))

            # add the parent to the generation
            for element in chosen_ones:
                new_population.append(element)

            return new_population


    def remove_death(self):
        """
        Remove death individuals from population list
        :return: Updated population list
        """
        for i, indi in enumerate(self.population):
            if indi.get_life() is not True:
                self.population.pop(i)

    def save_best(self):
        best = self.__selection__()[0]
        return best

    def mass_prediction(self):
        proc = []
        for bird in self.population:
            p = Process(target=bird.predict())
            p.start()
            proc.append(p)

        for p in proc:
            p.join()

    def mass_fall(self, grav):
        proc = []
        for bird in self.population:
            p = Process(target=bird.falling(grav))
            p.start()
            proc.append(p)

        for p in proc:
            p.join()

