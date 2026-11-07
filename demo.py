from problems import Gridworld, SinglePlayerGame
from algorithms import RandomAgent

"""
Demo: random agent attempting each problem
"""

demo_moves = 30
demo_delay = 0.1
baseline_games = 20


def showOneGame(name, problem):
    print(f"--- {name}: random agent and up to {demo_moves} moves ---")
    SinglePlayerGame(problem, RandomAgent(), maxMoves=demo_moves, delay=demo_delay).playGame()
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
          f"average reward {sum(rewards) / n:.2f} + average moves {sum(movesUsed) / n:.0f}")


if __name__ == "__main__":
    showOneGame("Gridworld 8x8", Gridworld(size=8, seed=0))

    print(f"--- Random agent baseline + {baseline_games} games per size ---")
    for size in (5, 10, 20, 40):
        summarize(f"Gridworld {size}x{size}", Gridworld(size=size, seed=0))