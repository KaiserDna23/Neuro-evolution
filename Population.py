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


    def cal_fitness(self):
        """
        Calculate and assign fitness based on score of individuals, the fitness is calculated as follows:
        fit = score/sum_score.
        This ensures that every value will be < 1, and so doing, represents each bird probability of being chosen.
        """
        sum_ = 0
        sorted_ = {}
        # Get the sum of all scores
        for i in range(0, len(self.population)):
            sum_ += self.population[i].get_score()

        for i in range(0, len(self.population)):
            if self.population[i].get_score() <= 0 or sum <= 0:
                fitness = 0
                self.population[i].set_fitness(fitness)
                sorted_.update({str(fitness) : self.population[i]})

            else:
                fitness = self.population[i].get_score()/sum_
                self.population[i].set_fitness(int(fitness))
                sorted_.update({str(fitness) : self.population[i]})

        print(self.population)
        print(sorted_)
        print(sorted_.keys())
        self.highest_fitness = sorted(list(sorted_.keys()))[0]


    def __selection__(self):
        """
        Select the best couple of individuals performing well.
        :return: chosen_ones, a couple of individuals
        """
        scores_ = {}


        if len(self.population) >= 1:
            # Relate score to individual, then sort by score
            for i in range(0, len(self.population)):
                scores_.update({str(self.population[i].get_fitness()): self.population[i]})

            # Sort the keys(fitness score) in reverse order and then return the highest
            keys = sorted(list(scores_.keys()), reverse=True)
            # With keys sorted the best/ highest is located at first position
            key = keys[0]
            self.best_score = scores_[key].get_score()
            return scores_[key]

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



    # Matting pool
    def matting_pool(self):
        """
        Perform matting on population individuals.
        Choose the best 2 and make them share their weights with the rest of the population.

        :return: new_population,  a list containing the new generation
        """
        new_population = []
        chosen_one = self.__selection__()
        # Use most fitted instances to reproduce with
        if len(self.population) >= 1:
            for element in self.population:
                if chosen_one is not element:
                        x_, y_ = self.__rand_position__()
                        new_population.append(Bird(x_, y_, parents=[chosen_one, element]).mutation(0.1))

            # add the parent to the generation
            new_population.append(chosen_one)

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

