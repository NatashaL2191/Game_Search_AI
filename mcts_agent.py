import math
import random


class MCTSNode:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = state.get_legal_moves()

    def is_fully_expanded(self):
        """Return True if every legal move from this state has a corresponding child."""
        return len(self.untried_moves) == 0

    def best_child(self, c=1.41):
        """Return the child with the highest UCB1 score."""
        return max(
            self.children,
            key=lambda child: (child.wins / child.visits)
                              + c * math.sqrt(math.log(self.visits) / child.visits)
        )

    def best_move(self):
        """Return the move leading to the child with the most visits."""
        return max(self.children, key=lambda child: child.visits).move


# ---------------------------------------------------------------------------
# The four MCTS steps
# ---------------------------------------------------------------------------

def select(node):
    """
    Starting from the given node, descend through fully-expanded,
    non-terminal nodes by always picking the best child (UCB1).
    Stop at the first node that still has untried moves or is terminal.
    """
    while node.is_fully_expanded() and not node.state.is_terminal():
        node = node.best_child()
    return node


def expand(node):
    """
    Choose one untried move at random, apply it to get a new state,
    create the corresponding child node, attach it to the tree, and
    return the new child.
    """
    move = random.choice(node.untried_moves)
    node.untried_moves.remove(move)

    new_state = node.state.make_move(move)
    child = MCTSNode(new_state, parent=node, move=move)
    node.children.append(child)
    return child


def simulate(state):
    """
    From the given state, play a random game to completion.
    At each step choose a uniformly random legal move.
    Return the utility of the terminal state.
    """
    current_state = state
    while not current_state.is_terminal():
        move = random.choice(current_state.get_legal_moves())
        current_state = current_state.make_move(move)
    return current_state.utility()


def backpropagate(node, result):
    """
    Walk from the given node up to the root.
    - Increment the visit count of every node.
    - Increment the win count only for nodes where the result was
      favorable for the player who just moved into that node.
    """
    current = node
    while current is not None:
        current.visits += 1
        # After make_move, current_player has already flipped to the NEXT player.
        # So the player who moved INTO this node is current_player * -1.
        # We credit a win when that player matches the simulation result.
        mover = current.state.current_player * -1
        if result == mover:
            current.wins += 1
        current = current.parent


# ---------------------------------------------------------------------------
# Main MCTS loop
# ---------------------------------------------------------------------------

def mcts(state, iterations=1000):
    """
    Run Monte Carlo Tree Search for the given number of iterations and
    return the best move found from the root state.
    """
    root = MCTSNode(state)

    for _ in range(iterations):
        # 1. Select – find a promising leaf
        leaf = select(root)

        # 2. Expand – grow the tree (skip if terminal)
        if not leaf.state.is_terminal():
            leaf = expand(leaf)

        # 3. Simulate – play a random game from the new leaf
        result = simulate(leaf.state)

        # 4. Back-propagate – update statistics up the path to the root
        backpropagate(leaf, result)

    return root.best_move()