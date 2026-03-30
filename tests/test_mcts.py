# to run:
# use terminal: python -m tests.test_mcts
from tic_tac_toe import TicTacToe
from mcts_agent import mcts

def make_board(board, player):
    """Helper to set up a custom board position."""
    game = TicTacToe()
    game.board = board
    game.current_player = player
    return game



# --- Test 4: MCTS vs MCTS full game ends legally ---
print("\nTest 4 – full MCTS vs MCTS game:")
state = TicTacToe()
while not state.is_terminal():
    m = mcts(state, iterations=300)
    state = state.make_move(m)
state.display()
result = state.utility()
assert result in (-1, 0, 1), f"Test 4 failed: invalid result {result}"
print(f"Result: {'X wins' if result==1 else 'O wins' if result==-1 else 'Draw'} ✓")

# --- Test 5: MCTS never plays an illegal move ---
print("\nTest 5 – checking all moves are legal:")
for game_num in range(20):
    state = TicTacToe()
    while not state.is_terminal():
        legal = state.get_legal_moves()
        m = mcts(state, iterations=100)
        assert m in legal, f"Illegal move {m} played in game {game_num}!"
        state = state.make_move(m)
print("Test 5 passed – no illegal moves in 20 games ✓")

print("\nTest 6 – full MCTS vs MCTS game:100 iterations:")
state = TicTacToe()
while not state.is_terminal():
    m = mcts(state, iterations=100)
    state = state.make_move(m)
state.display()
result = state.utility()
assert result in (-1, 0, 1), f"Test 4 failed: invalid result {result}"
print(f"Result: {'X wins' if result==1 else 'O wins' if result==-1 else 'Draw'} ✓")

print("\nTest 7 – full MCTS vs MCTS game:1000 iterations:")
state = TicTacToe()
while not state.is_terminal():
    m = mcts(state, iterations=1000)
    state = state.make_move(m)
state.display()
result = state.utility()
assert result in (-1, 0, 1), f"Test 4 failed: invalid result {result}"
print(f"Result: {'X wins' if result==1 else 'O wins' if result==-1 else 'Draw'} ✓")

print("\nTest 8 – full MCTS vs MCTS game:10000 iterations:")
state = TicTacToe()
while not state.is_terminal():
    m = mcts(state, iterations=10000)
    state = state.make_move(m)
state.display()
result = state.utility()
assert result in (-1, 0, 1), f"Test 4 failed: invalid result {result}"
print(f"Result: {'X wins' if result==1 else 'O wins' if result==-1 else 'Draw'} ✓")

print("\nAll tests passed!")