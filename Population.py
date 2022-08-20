# Population class

from multiprocessing import Process
from random import randint

from Bird import Bird


class Population:
    width_screen = 576
    height_screen = 800

    def __init__(self, nber_individuals:int):
        self.population = []
        self.extinct = False
        self.generations_scores = {}
        self.highest_fitness = 0
        self.best_score = 0
        self.__generate_population__(nber_individuals)

    #################################################################
    ################## Class Methods
    ################################################################

    # get population
    def get_population(self):
        return self.population

    # get the best score
    def get_best_score(self):
        return self.best_score

    # return highest fitness score
    def get_best_fitness(self):
        return self.highest_fitness

    # get extinct
    def get_extinct(self):
        return True if len(self.population) <= 0 else False

    # set the extinction alarm
    def set_extinct(self):
        self.extinct = True

    # set population
    def set_population(self, population):
        self.population = population

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

        #self.best_score = self.population[0]



            # if len(keys) >= 1:
            #     for key in keys[:2]:
            #         sorted_population.append(scores_[key])
            #     # Get and set the best score in generation
            #     #self.best = sorted_population[0].get_score()
            #     return [sorted_population[0], sorted_population[1]]
            # else:
            #     sorted_population.append(scores_[keys[0]])
            #     # Get and set the best score in generation
            #     #self.best = sorted_population[0].get_score()
            #     return [sorted_population[0]]


    def remove_death(self):
        """
        Remove death individuals from population list
        :return: Updated population list
        """
        for i, indi in enumerate(self.population):
            if indi.get_life() is not True:
                self.population.pop(i)

    def save_best(self):
        best = self.__selection__()
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

    def set_highestFitness(self, param):
        self.highest_fitness = param

