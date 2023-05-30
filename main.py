import os
from time import sleep
from flappybird import FlappyBird


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')

    for s in range(1, 6):
        print(f'The game starts in {s} seconds...')
        sleep(1)

    flappy_game = FlappyBird()
    flappy_game.run(config_file=config_path)
