import math
import random

import numpy as np
# ----- Importing Game framework
import pygame as game
import tensorflow as tf
from tensorflow import keras
from keras import layers

# Suppress prediction warning
from tensorflow import compat
from tensorflow.python.keras import Input

compat.v1.disable_eager_execution()


# imports
# ---- Importing Machine Learning Framework


class Bird:
    """
    Class describing the bird object of the game with its method.
    The class object is said to have a brain, which is defined by either a NEAT or a neural network
    """

    # class attributes
    lift_force = -1
    brain = None
    image = "Images/bluebird-downflap.png"

    # Constructor
    def __init__(self, x, y, **kwargs) -> None:

        if 'parents' in kwargs:
            self.parent1 = kwargs['parents'][0]
            self.parent2 = kwargs['parents'][1]
            self.brain = self.create_brain()
            parent1_brain = self.parent1.getBrain()
            parent2_brain = self.parent2.getBrain()

            if self.parent1.isDominant:

                for i in range(0, len(self.brain.layers) - 1):
                    # Have the weights of each layer per parent
                    limit = int(len(parent2_brain.layers[i]) * 0.2)
                    parent1_layer = parent1_brain.layers[i][limit:]  # get 80% of the weight of the first parent
                    parent2_layer = parent2_brain.layers[i][:limit]  # get 20% of the weight of the second parent
                    base_weight = np.concatenate((parent2_layer, parent1_layer),
                                                 axes=0)  # Concatenate the 2 arrays horizontally

                    # Save the weight on the layer
                    self.brain.layers[i].set_weights(base_weight)

            for i in range(0, len(self.brain.layers) - 1):
                # Have the weights of each layer per parent
                limit = int(len(parent2_brain.layers[i]) * 0.2)
                parent1_layer = parent1_brain.layers[i][:limit]  # get 20% of the weight of the first parent
                parent2_layer = parent2_brain.layers[i][limit:]  # get 80% of the weight of the second parent
                base_weight = np.concatenate((parent1_layer, parent2_layer),
                                             axes=0)  # Concatenate the 2 arrays horizontally

                # Save the weight on the layer
                self.brain.layers[i].set_weights(base_weight)
        else:
            # If there's no parent create a brain to use
            self.brain = self.create_brain()

        # Bird's physical property
        self.isalive = True
        self.x_position = x
        self.y_position = y
        self.falling_speed = 0
        self.image_count = 0
        self.gravity = 0

        self.incoming_pipes = []
        self.score = 0
        self.fitness_score = 0
        # Genes properties
        self.isDominant = False
        # Bird's image
        self.image = game.image.load(r"Images/bluebird-downflap.png").convert_alpha()
        self.image = game.transform.scale2x(self.image)
        self.bird_rect = self.image.get_rect()

    # --- Class Methods ---#

    # Get mask for collision
    def get_mask(self):
        return game.mask.from_surface(self.image)

    def set_gravity(self, grav):
        self.gravity = grav

    # Assert the bird itself to check if it collied against a pipe
    def check_collision(self, pipe_rect):
        if self.bird_rect.colliderect(pipe_rect):
            self.isalive = False
            return True
        return False

    # reset the bird's velocity
    def reset_moves(self):
        self.falling_speed = 0

    # add 1 to the bird's score (fitting score)
    def add_score(self):
        self.score += 1

    # Get life
    def get_life(self):
        return self.isalive

    # Get the score
    def get_score(self):
        return self.score

    # Get the fitness score
    def get_fitness(self):
        return self.fitness_score

    # Get the bird's rectangle
    def get_rec(self):
        return self.bird_rect

    # Set incoming pipes
    def set_incoming_pipes(self, pipeslist):
        self.incoming_pipes = pipeslist

    # set position
    def position(self, x, y) -> None:
        """ Setting the birds position manually """
        self.x_position = x
        self.y_position = y

    # Jump provides the bird with flying ability
    def jump(self):
        self.falling_speed += self.lift_force

    # put the bird in motion by decreasing its velocity
    def falling(self, gravity: float):
        self.falling_speed += gravity
        self.falling_speed *= 0.9
        self.y_position += self.falling_speed

    # Draw
    def draw(self, screen):
        self.image_count += 1
        screen.blit(self.image, (self.x_position, self.y_position))

    # Make the bird die
    def die(self):
        """
        Change state of variable
        :return: alive becomes False
        """
        if self.isalive is True:
            self.isalive = False

    # Restore live
    def restore_life(self):
        """
        Restore life, set the live variable to True
        :return:
        """
        isalive = True

    # Collision detection based on distance between two coordinates equation
    def hasColleid(self, pipe_x, pipe_y):
        distance = math.sqrt((math.pow(pipe_x - self.x_position, 2)) + (math.pow(pipe_y - self.y_position, 2)))
        # if the distance is < to 30 pixels return true
        if distance <= 30:
            print("HIT")
            return True
        if self.y_position >= 900 or self.y_position <= 0:
            return True
        return False

    # function to determine if player has score a point
    def grant_score(self, pipe1_rect) -> bool:
        """
        Determine if the player has successfully passed in between the 2 pipes
        Since the 2 pipes have nearly same X position while focus the if clause on the fact that the players' y coordinate has to be between the top y and bottom y.
        :param pipe1_rect: Pipe 1 rectangle object
        :return: player's score + 1
        """
        top_pipe, bottom_pipe = pipe1_rect.get_rectangles()
        top_y = top_pipe.top
        top_x = top_pipe.left
        bottom_y = bottom_pipe.top
        bottom_x = bottom_pipe.left

        # print(top_y, bottom_y)
        if self.x_position == top_x or self.x_position == bottom_x:
            if top_y < self.y_position < bottom_y:
                self.add_score()
                return True
        return False

    # Create brain using neural nets with backpropagation
    def create_brain(self):
        """
        Create the brain using neural networks, it takes a list of parameters, which include the y position of the bird,
        the x position of the upper or lower pipe, and  the distance of the bird from the pipes
        :return: A Tensorflow.keras sequential model
        """

        model = keras.Sequential([
            layers.Input(shape=(5,)),
            layers.Dense(8, activation="tanh", name="input_layer"),
            layers.Dense(1, activation="sigmoid", name="Last_layer"),
        ])

        return model

    # Get the different layers of the model
    def __get_layers__(self):
        if self.brain is not None:
            return self.brain.layers[0], self.brain.layers[1], self.brain.layers[2]

        return True

    # return neural network input
    def __nn_input__(self):
        # print("> PIPE in BIRD ", self.incoming_pipes)
        if len(self.incoming_pipes) >= 1:
            pipe_x = self.incoming_pipes[0].x
            pipe_h = self.incoming_pipes[0].height
            pipe_b = self.incoming_pipes[0].bottom
        else:
            pipe_x = 0
            pipe_h = 0
            pipe_b = 0

        # pipe_x = self.incoming_pipes[0].left if self.incoming_pipes is not [] else 0  # if there's no pipe yet create replace with None or empty with 0
        distance_from_pipe = abs(pipe_x - self.x_position)
        top_height = abs(self.y_position - pipe_h)
        bottom_height = abs(self.y_position - pipe_b)
        result = np.array([[self.y_position, pipe_x, distance_from_pipe, top_height, bottom_height]])
        return result

    # Normalise the input from 0-1, to reduce variance
    def norm(self, lis):
        """
        Normalize the inputs in between 0 and 1
        :param lis: List of parameters
        :return: List containing parameters normalized between 0 and 1
        """
        lis_norm = (lis - lis.min()) / (lis.max() - lis.min())
        # print(lis_norm)
        return lis_norm

    # Return the brain
    def getBrain(self):
        return self.brain

    # Predict next move
    def predict(self):
        """
         Create the brain using neural networks, it takes a list of parameters, which include the x position, y position of the bird, the x position of the upper or
         lower pipe, and  the distance of the bird from the pipes, we'll feed forward the neural network, and it's result is squeezed in between 0-1,
         if the result is >= 0.5, make result = 1 else 0


        :return: int (either 1 or 0)
        """

        input_list = self.__nn_input__()
        normalized_input = self.norm(input_list)
        model = self.create_brain()

        choice = model.predict(normalized_input)

        choice = 1 if choice > 0.5 else 0
        print("Up -1" if choice == 1 else "Down -0")
        if choice == 1:
            self.jump()

    def __mutation__(self, val, mutation_rate: float):
        if random.uniform(0, 1) > mutation_rate:
            # slightly modify the value
            return lambda x: x + random.uniform(-0.1, 0.1)(val)
        else:
            return val

    def mutation(self, mutation_rate: float):
        """
        Base on the mutation rate a random number is drawn if the random number is greater
        than the mutation rate, perform mutation on the input and hidden layer only,
        alter sightly the value of the weights, between -0.1 and 0.1, this is done not to
        drastically change weights performing well and kickstart those who don't.

        :param mutation_rate: float representing the mutation rate of the population
        :return: The instance of brain being mutated
        """
        if self.brain is not None:
            # Mutating 1st layer
            self.brain.layers[0].set_weights(self.__mutation__(self.brain.layers[0].weights, mutation_rate))
            # self.brain.layer[0].set_weights(self.__mutation__(self.brain.layers[0].bias.numpy(), mutation_rate))
            # Mutating 2nd layer
            self.brain.layers[1].set_weights(self.__mutation__(self.brain.layers[0].weights, mutation_rate))
            # self.brain.layers[1].set_weights(self.__mutation__(self.brain.layers[0].weights, mutation_rate))

    def set_fitness(self, fitness):
        """
        Add fitness score to bird, related to how well the bird is performing
        :param fitness: int, score representing how well the bird is performing.
        """
        self.fitness_score = fitness

