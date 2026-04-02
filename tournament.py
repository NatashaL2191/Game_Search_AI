import random
import time
from Game import TicTacToe
import minimax_agent
from mcts_agent import mcts

# --- Agent wrappers ---


def random_agent(state):
    """Pick a uniformly random legal move."""
    return random.choice(state.get_legal_moves())


def minimax_agent_wrapper(state):
    """Wrapper for plain minimax."""
    return minimax_agent.minimax(state)


def minimax_ab_agent_wrapper(state):
    """Wrapper for alpha-beta minimax."""
    return minimax_agent.minimax_ab(state)


def mcts_agent(iterations=1000):
    """Return an MCTS agent closure with a fixed iteration count."""
    def agent(state):
        return mcts(state, iterations=iterations)
    agent.__name__ = f"MCTS({iterations})"
    return agent

# --- Single game ---


def play_game(x_agent, o_agent):
    """
    Play one game. x_agent and o_agent are callables: state -> move.
    Returns (winner, x_time, o_time) where winner in {1, -1, 0}
    and x_time/o_time are total seconds spent by each agent.
    """
    state = TicTacToe()
    x_time = 0.0
    o_time = 0.0

    while not state.is_terminal():
        if state.current_player == 1:
            t0 = time.perf_counter()
            move = x_agent(state)
            x_time += time.perf_counter() - t0
        else:
            t0 = time.perf_counter()
            move = o_agent(state)
            o_time += time.perf_counter() - t0
        state = state.make_move(move)

    return state.utility(), x_time, o_time

# --- Tournament ---


def run_matchup(x_agent, o_agent, n_games=100, label=None):
    """
    Play n_games between x_agent and o_agent.
    Print a result summary and return (x_wins, o_wins, draws).
    """
    x_wins = o_wins = draws = 0
    total_x_time = total_o_time = 0.0

    for _ in range(n_games):
        result, xt, ot = play_game(x_agent, o_agent)
        total_x_time += xt
        total_o_time += ot
        if result == 1:
            x_wins += 1
        elif result == -1:
            o_wins += 1
        else:
            draws += 1

    avg_x = total_x_time / n_games
    avg_o = total_o_time / n_games

    x_name = getattr(x_agent, '__name__', 'X')
    o_name = getattr(o_agent, '__name__', 'O')
    title = label or f"{x_name} vs {o_name}"

    print(f"\n{'─' * 55}")
    print(f"  {title}  ({n_games} games)")
    print(f"{'─' * 55}")
    print(f"  X wins : {x_wins:3d}  ({x_wins/n_games*100:.1f}%)")
    print(f"  O wins : {o_wins:3d}  ({o_wins/n_games*100:.1f}%)")
    print(f"  Draws  : {draws:3d}  ({draws/n_games*100:.1f}%)")
    print(f"  Avg time/game — X: {avg_x:.4f}s  O: {avg_o:.4f}s")

    return x_wins, o_wins, draws

# --- Timing Experiment ---


def timing_experiment(iteration_counts=(100, 500, 1000, 5000, 10000), n_games=10):
    """
    Measure average time per move for MCTS at different iteration counts.
    Compare against minimax alpha-beta.
    """
    print("\n" + "=" * 55)
    print("  MCTS Timing Experiment")
    print("=" * 55)
    print(f"  {'Agent':<22} {'Avg time/game':>14}  {'Avg time/move':>14}")
    print(f"  {'-'*22}  {'-'*14}  {'-'*14}")

    # Minimax alpha-beta baseline
    total = 0.0
    move_total = 0
    for _ in range(n_games):
        state = TicTacToe()
        moves_made = 0
        while not state.is_terminal():
            t0 = time.perf_counter()
            move = minimax_ab_agent_wrapper(state)
            total += time.perf_counter() - t0
            state = state.make_move(move)
            moves_made += 1
        move_total += moves_made
    avg_game = total / n_games
    avg_move = total / move_total
    print(f"  {'Minimax (alpha-beta)':<22} {avg_game:>14.4f}s  {avg_move:>14.6f}s")

    # MCTS at each iteration count
    for iters in iteration_counts:
        total = 0.0
        move_total = 0
        agent = mcts_agent(iters)
        for _ in range(n_games):
            state = TicTacToe()
            moves_made = 0
            while not state.is_terminal():
                t0 = time.perf_counter()
                move = agent(state)
                total += time.perf_counter() - t0
                state = state.make_move(move)
                moves_made += 1
            move_total += moves_made
        avg_game = total / n_games
        avg_move = total / move_total
        print(f"{f'MCTS({iters})':<22} {avg_game:>14.4f}s  {avg_move:>14.6f}s")


# --- Main ---
if __name__ == '__main__':
    N = 100  # games per matchup

    # Give agents display names
    random_agent.__name__ = "Random"
    minimax_agent_wrapper.__name__ = "Minimax"
    minimax_ab_agent_wrapper.__name__ = "Minimax_AB"

    mcts1000 = mcts_agent(1000)
    mcts1000.__name__ = "MCTS(1000)"

    print("=" * 55)
    print("  TOURNAMENT — Tic-Tac-Toe")
    print("=" * 55)

    # --- Node counting on empty board ---
    print("\nRunning node count on empty board...")

    minimax_agent.nodes_minimax = 0
    minimax_agent.nodes_ab = 0

    # Plain minimax
    minimax_agent_wrapper(TicTacToe())
    print(f"Plain minimax nodes evaluated: {minimax_agent.nodes_minimax}")

    # Alpha-beta minimax
    minimax_ab_agent_wrapper(TicTacToe())
    print(f"Alpha-beta minimax nodes evaluated: {minimax_agent.nodes_ab}")

    # Percentage pruned
    pruned_pct = (minimax_agent.nodes_minimax -
                  minimax_agent.nodes_ab) / minimax_agent.nodes_minimax * 100
    print(f"Percentage of nodes pruned: {pruned_pct:.2f}%")

    # --- Matchups ---
    run_matchup(minimax_ab_agent_wrapper, random_agent, N,
                label="Minimax_AB (X) vs Random (O)")
    run_matchup(mcts1000, random_agent, N,
                label="MCTS(1000) (X) vs Random (O)")
    run_matchup(minimax_ab_agent_wrapper, mcts1000, N,
                label="Minimax (X) vs MCTS(1000) (O)")
    run_matchup(mcts1000, minimax_ab_agent_wrapper, N,
                label="Minimax (X) vs MCTS(1000) (O)")

    # --- Timing experiment ---
    timing_experiment()
