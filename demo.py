'''
Demo for a random agent attempting each problem
'''

from problems import Gridworld, Snake, SinglePlayerGame
from algorithms import RandomAgent

demo_delay = 0.1
baseline_games = 20


def showOneGame(name, problem, maxMoves, stopAtScore=None):
    print(f"--- {name}: random agent ---")
    SinglePlayerGame(problem, RandomAgent(), maxMoves=maxMoves, delay=demo_delay,
                     stopAtScore=stopAtScore).playGame()
    print()


def summarize(name, problem):
    scores, rewards, movesUsed = [], [], []
    for _ in range(baseline_games):
        score, reward, moves = SinglePlayerGame(problem, RandomAgent(), verbose=False).playGame()
        scores.append(score)
        rewards.append(reward)
        movesUsed.append(moves)
    n = baseline_games
    print(f"{name}: average score {sum(scores) / n:.2f}, "
          f"average reward {sum(rewards) / n:.2f}, average moves {sum(movesUsed) / n:.0f}")


if __name__ == "__main__":
    showOneGame("Gridworld 8x8 - 30-move cap", Gridworld(size=8, seed=0), maxMoves=30)
    showOneGame("Snake 5x5 - stops at 2 apples or death", Snake(size=5, seed=0), maxMoves=100, stopAtScore=2)

    print(f"--- Random agent baseline, {baseline_games} games per size ---")
    for size in (5, 10, 20, 40):
        summarize(f"Gridworld {size}x{size}", Gridworld(size=size, seed=0))
    for size in (4, 5, 6):
        summarize(f"Snake {size}x{size}", Snake(size=size, seed=0))