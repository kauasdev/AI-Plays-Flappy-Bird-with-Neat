import pygame
import pyautogui
import neat
import math
import os
from flappybird.Base import Base
from flappybird.Pipe import Pipe
from flappybird.Bird import Bird


class FlappyBird:
    gen = 0
    pygame.font.init()  # Init font
    pygame.display.init()
    pygame.display.set_caption("Flappy Bird")

    def __init__(self):
        self.window_width = self.get_window_w_h()[0]
        self.window_height = self.get_window_w_h()[1]
        self.__window = pygame.display.set_mode((self.window_width, self.window_height))
        self.floor = 650
        self.stat_font = pygame.font.SysFont("comicsans", 50)
        self.end_font = pygame.font.SysFont("comicsans", 70)
        self.draw_lines = False
        self.IMGS = self.__get_images()

    @staticmethod
    def get_window_w_h() -> tuple[int, int]:
        """
        Returns the height and one-third of the width of the screen
        :return: (window_width:int, window_height:int)
        """
        window_width, window_height = pyautogui.size()
        window_width = math.ceil(window_width / 3)

        return window_width, window_height

    @staticmethod
    def __get_images() -> {pygame.Surface}:
        current_path = os.getcwd()
        # Load images with pygame
        bg_img = pygame.transform.scale(pygame.image.load(
            os.path.join(current_path, "images/bg.png")
        ).convert_alpha(), (600, 900))
        base_img = pygame.transform.scale2x(pygame.image.load(
            os.path.join(current_path, "images/base.png")
        ).convert_alpha())
        pipe_img = pygame.transform.scale2x(pygame.image.load(
            os.path.join(current_path, "images/pipe.png")
        ).convert_alpha())
        bird_imgs = [pygame.transform.scale2x(pygame.image.load(
            os.path.join(current_path, f"images/bird{i}.png")
        )) for i in range(1, 4)]

        return {
            "BG": bg_img,
            "BASE": base_img,
            "PIPE": pipe_img,
            "BIRDS": bird_imgs
        }

    def __draw_window(
            self,
            window: pygame.Surface,
            birds: [Bird],
            pipes: [Pipe],
            base: Base,
            score=0,
            gen=0,
            pipe_ind=0
    ):
        """
        Draws the windows for the main game loop
        :param window: pygame window surface
        :param birds: List of birds
        :param pipes: List of pipes
        :param score: score of the game (int)
        :param gen: current generation
        :param pipe_ind: index of closest pipe
        :return: None
        """
        if gen == 0:
            gen = 1

        window.blit(self.IMGS['BG'], (0, 0))

        for pipe in pipes:
            pipe.draw(window)

        base.draw(window)
        for bird in birds:
            # Draw lines from bird to pipe
            if self.draw_lines:
                try:
                    pygame.draw.line(window, (255, 0, 0),
                                     (bird.x + bird.img.get_width() / 2, bird.y + bird.img.get_height() / 2), (
                                         pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width() / 2,
                                         pipes[pipe_ind].height), 5)
                    pygame.draw.line(window, (255, 0, 0),
                                     (bird.x + bird.img.get_width() / 2, bird.y + bird.img.get_height() / 2), (
                                         pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width() / 2,
                                         pipes[pipe_ind].bottom), 5)
                except ValueError:
                    pass
                except TypeError:
                    pass
                # Draw bird
            bird.draw(window)

        # Score
        score_label = self.stat_font.render(
            f"Score: {score}",
            True, (255, 255, 255)
        )
        window.blit(score_label, (self.window_width - score_label.get_width() - 15, 10))

        # Generations
        score_label = self.stat_font.render("Gens: " + str(gen - 1), True, (255, 255, 255))
        window.blit(score_label, (10, 10))

        # alive
        score_label = self.stat_font.render("Alive: " + str(len(birds)), True, (255, 255, 255))
        window.blit(score_label, (10, 50))

        pygame.display.update()

    def eval_genomes(self, genomes, config):
        """
        Runs the simulation of the current population of
        birds and sets their fitness based on the distance they
        reach in the game.
        """
        # start by creating lists holding the genome itself, the
        # neural network associated with the genome and the
        # bird object that uses that network to play
        nets = []
        birds = []
        ge = []

        for genome_id, genome in genomes:
            genome.fitness = 0  # start with fitness level of 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            birds.append(Bird(230, 350, bird_imgs=self.IMGS['BIRDS']))
            ge.append(genome)

        base = Base(self.floor, base_img=self.IMGS['BASE'])
        pipes = [Pipe(700, pipe_img=self.IMGS['PIPE'])]
        score = 0

        clock = pygame.time.Clock()

        running = True
        while running and len(birds) > 0:
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()
                    break

            pipe_ind = 0
            if len(birds) > 0:
                if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                    # determine whether to use the first or second
                    pipe_ind = 1  # pipe on the screen for neural network input

            for x, bird in enumerate(birds):  # give each bird a fitness of 0.1 for each frame it stays alive
                ge[x].fitness += 0.1
                bird.move()

                # send bird location, top pipe location and bottom pipe
                # location and determine from network whether to jump or not
                output = nets[birds.index(bird)].activate(
                    (bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

                if output[0] > 0.5:
                    # we use a hyperbolic tangent activation function so result will be
                    # between -1 and 1. if over 0.5 jump
                    bird.jump()

            base.move()

            rem = []
            add_pipe = False
            for pipe in pipes:
                pipe.move()
                # check for collision
                for bird in birds:
                    if pipe.collide(bird, self.__window):
                        ge[birds.index(bird)].fitness -= 1
                        nets.pop(birds.index(bird))
                        ge.pop(birds.index(bird))
                        birds.pop(birds.index(bird))

                    if not pipe.passed and pipe.x < bird.x:
                        pipe.passed = True
                        add_pipe = True

                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    rem.append(pipe)

            if add_pipe:
                score += 1
                # can add this line to give more reward for passing through a pipe (not required)
                for genome in ge:
                    genome.fitness += 5
                pipes.append(Pipe(self.window_width+250, pipe_img=self.IMGS['PIPE']))

            for r in rem:
                pipes.remove(r)

            for bird in birds:
                if bird.y + bird.img.get_height() - 10 >= self.floor or bird.y < -50:
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))

            self.__draw_window(self.__window, birds, pipes, base, score, self.gen, pipe_ind)

            # break if score gets large enough
            '''if score > 20:
                pickle.dump(nets[0],open("best.pickle", "wb"))
                break'''

    def run(self, config_file):
        """
        Runs the NEAT algorithm to train a neural network to play flappy bird.
        :param config_file: location of config file
        :return: None
        """
        config = neat.config.Config(
            neat.DefaultGenome, neat.DefaultReproduction,
            neat.DefaultSpeciesSet, neat.DefaultStagnation,
            config_file
        )

        # Create the population, which is the top-level object for a NEAT run.
        p = neat.Population(config)

        # Add a stdout reporter to show progress in the terminal.
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        # p.add_reporter(neat.Checkpointer(5))

        # Run for up to 50 generations.
        winner = p.run(self.eval_genomes, 50)

        # show final stats
        print('\nBest genome:\n{!s}'.format(winner))
