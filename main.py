import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from core.game import Game


if __name__ == "__main__":
    game = Game()
    game.run()
