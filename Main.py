# imports
#---- Importing Machine Learning Framework
import datetime
import time
from multiprocessing import Process

import pygame as game

from Genetic_evaluation import GeneticEvaluation
from Pipe import Pipe, Base
# Importing Game framework
from Population import Population

# initialise font
game.font.init()




#########################################################################
############################## Game variables ###########################
#########################################################################

# time out
old_time = datetime.datetime.now()
timeout_flag = False


# intialise the game
game.init()
clock = game.time.Clock()

# Texts
STATS = game.font.SysFont("comicsans", 50)

# physics
gravity = 2

# Creating the game screen
width =  576
length = 850
screen = game.display.set_mode((width, length))

# Creating the background of the game and make the  image fit into the screen
background = game.image.load(r'Images/background-day.png').convert_alpha()
background = game.transform.scale2x(background)

# Load game floor image and make it fit into the screen
floor_base = game.image.load(r'Images/base.png').convert_alpha()
floor_base = game.transform.scale2x(floor_base)
floor_x = 0

# Load pipe image and make it fit into the screen
pipe_image = game.image.load(r'Images/pipe-red.png').convert_alpha()
pipe_image = game.transform.scale2x(pipe_image)

pipe_height = [400, 600, 700]
pipe_list = []


#########################################################################
############################## Game Functions ###########################
#########################################################################

def draw_window(screen_, birds, pipes, base, score, count):
    screen_.blit(background, (0, 0))
    # for bird in birds:
    #     bird.draw(screen_)
    #
    # for pipe in pipes:
    #     pipe.draw(screen_)

    proc = []
    proc2 = []
    for bird in birds:
        p = Process(target=bird.draw(screen_))
        p.start()
        proc.append(p)

    for p in proc:
        p.join()

    for pipe in pipes:
    #    pipe.draw(screen_)
        p = Process(target=pipe.draw(screen_))
        p.start()
        proc2.append(p)

    for p in proc2:
        p.join()


    text = STATS.render("Score: "+ str(score), 1, (255, 255, 255))
    count_ = STATS.render("Generation: " + str(count), 1, (255, 255, 255))
    screen_.blit(count_, (width - 100 - text.get_width(), 10))
    screen_.blit(text, (width - 10 - text.get_width(), 50))

    base.draw(screen_)

    game.display.update()


# def mass_prediction(population, grav):
#     population.mass_fall(grav)
#     population.mass_prediction()

    # result.wait


def main(id : int, population):
    """
    Main program loop. Where the agent get challenged.

    :param id: Generation count
    :param population: Population list
    """

    generation_count = id
    population_ = population
    back_up = []
    screen_ = game.display.set_mode((width, length))
    birds = population_.get_population()
    pipes = [Pipe(550)]
    base_ = Base(650)
    end_clock = 0
    score = 0
    running_ = True

    # start timing
    start_clock = time.perf_counter()

    # game loop
    while running_:

        clock.tick(600)
        for event_ in game.event.get():
            if event_.type == game.QUIT:
                running_ = False
                game.quit()
                quit()

            # if event_.type == game.KEYDOWN:
            #     if event_.key == game.K_SPACE:
            #         [bird.jump() for bird in birds]

        # Moving birds
        for bird in birds:
            #print(f"{type(bird)} : {bird}")
            bird.falling(gravity)
            # set incoming pipes
            bird.set_incoming_pipes(pipes)
            # give a bit of fitness
            #bird.fitness_score += 0.1

        # Prediction
        population_.mass_prediction()

        add_pipe = False
        remove_list = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collied(bird):
                    back_up.append(bird)
                    # remove the bird
                    birds.pop(x)

                # if bird passes underneath, success
                if not pipe.passed and pipe.x < bird.x_position:
                    pipe.passed = True
                    add_pipe = True

            # remove offset pipes
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove_list.append(pipe)

            pipe.move()

        # Create back another pipe since one is gone
        if add_pipe:
            for bird in birds:
                bird.add_score()
            pipes.append(Pipe(550))
            # bird has successfully pass, so increase point counter
            score += 1

        # remove pipes
        for r in remove_list:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            # check if we hit the floor
            if bird.y_position + bird.image.get_height() >= 650 or bird.y_position < 0:
                back_up.append(bird)
                birds.pop(x)


        # Check if population got extinct
        if len(birds) <= 0:
            end_clock = time.perf_counter()
            print('EXTINCT')
            running_ = False

        base_.move()
        draw_window(screen_, birds, pipes, base_,score, generation_count)

    # Calculate the time spend before gotten extinct
    time_taken = round(end_clock - start_clock, 2)

    return start_clock, end_clock, score, back_up

def run():
    # Create population
    population = Population(2)
    eval_pop = GeneticEvaluation(population, 5)
    eval_pop.run(main)
    #print(main(3))



if __name__ == "__main__":
    run()
