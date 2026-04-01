def minimax(state):
    """Return the best move for the current player (no pruning)."""
    if state.current_player == 1:
        best_value = float('-inf')
        best_move = None
        for move in state.get_legal_moves():
            child = state.make_move(move)
            value = min_value(child)
            if value > best_value:
                best_value = value
                best_move = move
        return best_move
    else:
        best_value = float('inf')
        best_move = None
        for move in state.get_legal_moves():
            child = state.make_move(move)
            value = max_value(child)
            if value < best_value:
                best_value = value
                best_move = move
        return best_move


def max_value(state):
    if state.is_terminal():
        return state.utility()
    v = float('-inf')
    for move in state.get_legal_moves():
        child = state.make_move(move)
        v = max(v, min_value(child))
    return v


def min_value(state):
    if state.is_terminal():
        return state.utility()
    v = float('inf')
    for move in state.get_legal_moves():
        child = state.make_move(move)
        v = min(v, max_value(child))
    return v


def minimax_ab(state):
    """Return the best move for the current player using alpha-beta pruning."""
    if state.current_player == 1:
        best_value = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        for move in state.get_legal_moves():
            child = state.make_move(move)
            value = min_value_ab(child, alpha, beta)
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, best_value)
        return best_move
    else:
        best_value = float('inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        for move in state.get_legal_moves():
            child = state.make_move(move)
            value = max_value_ab(child, alpha, beta)
            if value < best_value:
                best_value = value
                best_move = move
            beta = min(beta, best_value)
        return best_move


def max_value_ab(state, alpha, beta):
    if state.is_terminal():
        return state.utility()
    v = float('-inf')
    for move in state.get_legal_moves():
        child = state.make_move(move)
        v = max(v, min_value_ab(child, alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


def min_value_ab(state, alpha, beta):
    if state.is_terminal():
        return state.utility()
    v = float('inf')
    for move in state.get_legal_moves():
        child = state.make_move(move)
        v = min(v, max_value_ab(child, alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v