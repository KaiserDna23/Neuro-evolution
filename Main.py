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

def draw_window(screen_, birds, pipes, base, score):
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
    screen_.blit(text, (width - 10 - text.get_width(), 10))

    base.draw(screen_)

    game.display.update()


# def mass_prediction(population, grav):
#     population.mass_fall(grav)
#     population.mass_prediction()

    # result.wait


def main(population):
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
                    # reduce fitness score and don't favour bird that hit the pipe
                    #bird.fitness_score -= 1
                    # remove the bird
                    back_up.append(bird)
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
            #for bird in birds:
             #   bird.add_score()
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
        draw_window(screen_, birds, pipes, base_,score)

    # Calculate the time spend before gotten extinct
    time_taken = round(end_clock - start_clock, 2)

    return start_clock, end_clock, score, back_up

def run():
    # Create population
    population = Population(1)
    eval_pop = GeneticEvaluation(population, 5)
    eval_pop.run(main)
    #print(main(3))



if __name__ == "__main__":
    run()

#########################################################################
############################## Game variables ###########################
#########################################################################

#---

#
# timer_out = False
#
# running = True
#
# print(">> Initialisation ...")
#
# # Generate population
# generation = 0
# population = Population()
# population.generate_population(1)
#
#
# # Obstacle
# bottom_pipe, upper_pipe = create_pipes()
# # Pipe time, every 1.4 Sec
# pipe_time = game.USEREVENT
# game.time.set_timer(pipe_time, 1000)
#
#
# # Game loop
# ############
# while running:
#     # looping through every event
#     for event in game.event.get():
#         # if the event is closing then close
#         if event.type == game.QUIT:
#             game.quit()
#             sys.exit()
#
#         # if the event is a key press, and if the key is space jump
#         if event.type == game.KEYDOWN:
#             if event.key == game.K_SPACE:
#                 for indi in population.get_population():
#                     indi.jump()
#                     indi.predict()
#                     #print("Up -1" if action == 1 else "Down -0")
#
#
#         # if the event is the pipe time span, create new pipes
#         if event.type == pipe_time:
#             pipe_list.extend(create_pipes())
#
#     # Load background image
#     screen.blit(background, (0, 0))
#
#     # --- PIPES ---
#     draw_pipes(pipe_list)
#     move_pipes(pipe_list)
#
#     # Check for collision if collision occur the player dies, otherwise increase score
#     for i in range(len(pipe_list)-1):
#         pipe = pipe_list[i]
#         #if player.hasColleid(pipe.left, pipe.top):
#         for bird in population.get_population():
#             if bird.hasColleid(pipe.left, pipe.top):
#                 bird.die()
#
#         else:
#             for bird in population.get_population():
#                 bird.grantScore(pipe, pipe_list[i+1])
#
#     #--- PLAYER ---
#     # show player and move player
#     for bird in population.get_population():
#         screen.blit(bird.image, (bird.x_position, bird.y_position))
#         # Player movement
#         bird.falling(gravity)
#         # Update players pipe vision
#         bird.set_incoming_pipes(pipe_list)
#
#     ## Remove dead individuals before calculating the fitness score
#     population.remove_death()
#
#     # Set input parameters
#     # apply multiprocessing to speed computation
#
#     # Perform action
#     for bird in population.get_population():
#          bird.predict()
#
#
#
#     #
#     # for i in range(0, len(population.get_population())):
#     #     p = multiprocessing.Process(target=population.get_element(i).predict)
#     #     p.start()
#     #     process_list.append(p)
#     #
#     # for process in process_list:
#     #     process.join()
#     #
#     # with concurrent.futures.ProcessPoolExecutor() as executor:
#     #     result = [executor.submit(bird.predict) for bird in population.get_population()]
#     #     # Get result of the finished processes
#     #     for process in concurrent.futures.as_completed(result):
#     #         process.result()
#
#     # with concurrent.futures.ProcessPoolExecutor() as executor_:
#     #     executor_.map(predict, population.get_population())
#
#     # input_params = np.array([[bird.x_position, bird.y_position, pipe_x, distance_from_pipe]])
#
#
#
#     ## Perform fitness calculation
#     population.cal_fitness()
#
#     # If there's no population stop the program
#     if len(population.get_population()) == 0:
#         population.set_extinct()
#
#     if population.get_exinct() is True:
#         ## Create new generation
#         population = population.matting_pool()
#         generation += 1
#         print("New generation created")
#         print(f">> Generation {generation}")
#         print(f"Best score {population.get_best()}")
#         running = False
#
#     #counter(30, timeout_flag)
#
#     # Check if either population got extinct or timeout
#     #if timeout_flag is True:
#     #    running = False
#
#     game.display.update()
#     clock.tick(120)

####
# Methods

#Time out function
# def counter(timeout, timeout_flag):
#     """
#     Check if the time is exceeded.
#     :param timeout: time to work
#     """
#     flag = timeout_flag
#     if flag is not True:
#         print("Counter begins !")
#         global old_time
#         current_time_ = datetime.datetime.now()
#         desired_stop = (current_time_ + datetime.timedelta(minutes=timeout))#.strftime('%H:%M:%S')
#         while current_time_ != desired_stop:
#             if current_time_ != old_time:
#                 # Update the time
#                 old_time = current_time_
#     else:
#         # Timeout stop everything
#         flag = True
#
#
#
#
# # Set the floor into motion by providing 2 different images one after the other and both reducing them by one
# def floor(f_x) -> None:
#     """
#     Set the floor into motion.
#     Remember the screen ends that 576, so put another image right after its end and continue moving
#     """
#     screen.blit(floor_base, (f_x, 900))
#     screen.blit(floor_base, (f_x + 576, 900))
#
#
# # Create pipe
# def create_pipes() -> tuple:
#     """
#     Create both upper and lower pipe
#     :return: set of 2 types
#     """
#     random_pipe_pos = random.choice(pipe_height)
#     bottom_pipe = pipe_image.get_rect(midtop=(700, random_pipe_pos))
#     top_pipe = pipe_image.get_rect(midbottom=(700, random_pipe_pos - 300))
#     return bottom_pipe, top_pipe
#
#
# def move_pipes(pipelist) -> list:
#     """
#     Set the pipe image into motion by reducing it's X position by 5
#     """
#     for pipe in pipelist:
#         pipe.centerx -= 5
#     return pipelist
#
#
# # Draw pipes
# def draw_pipes(pipelist):
#     """
#     Draw the different pipe with the help of the pipe rectangles created with the function create_pipes().
#     If the bottom of the pipe touches the end of screen draw it straight, else flip the image and draw.
#     """
#     for pipe in pipelist:
#         if pipe.bottom >= 1024:
#             screen.blit(pipe_image, pipe)
#         else:
#             flip_pipe = game.transform.flip(pipe_image, False, True)
#             screen.blit(flip_pipe, pipe)
#
#
