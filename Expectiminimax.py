import math
from ThrowingSticks import stick_throw_probabilities
from copy import deepcopy
from GameState import GameState

class  Expectiminimax:
    def __init__(self, depth, ai_color="WHITE"):
        self.max_depth = depth
        self.ai_color = ai_color
        self.opponent_color = "BLACK" if ai_color == "WHITE" else "WHITE"

    def evaluate_heuristic(self, state):
        score = 0
        board = state.board

        if board.is_game_over():
            winner = board.get_winner()
            if winner == self.ai_color: return 10000
            else: return -10000

        score += (board.exited_pawns[self.ai_color] * 200)
        score -= (board.exited_pawns[self.opponent_color] * 200)

        for pawn in board.get_pawns_of_player(self.ai_color):
            if pawn.cell_id is not None:
                score += pawn.cell_id
                if pawn.cell_id in [26, 30]: score += 150
                elif pawn.cell_id == 27: score -= 100
                elif pawn.cell_id == 28:
                    score += (100 - (12/16) * (28 - 15))
                elif pawn.cell_id == 29:
                    score += (100 - (10/16) * (29 - 15))

        for pawn in board.get_pawns_of_player(self.opponent_color):
            if pawn.cell_id is not None:
                score -= pawn.cell_id
                if pawn.cell_id in [26, 30]: score -= 150
                elif pawn.cell_id == 27: score += 100
                elif pawn.cell_id == 28:
                    score -= (100 - (12/16) * (28 - 15))
                elif pawn.cell_id == 29:
                    score -= (100 - (10/16) * (29 - 15))
        return score

    def expectiminimax(self, state, depth, is_chance_node, current_dice=None):
        if depth == 0 or state.board.is_game_over():
            return self.evaluate_heuristic(state), None

        if is_chance_node:
            expected_value = 0
            probs = stick_throw_probabilities()
            for dice_val, prob in probs.items():
                val, _ = self.expectiminimax(state, depth - 1, False, dice_val)
                expected_value += prob * val
            return expected_value, None

        else:
            board = state.board
            movable_pawns = board.get_movable_pawns(current_dice)
            
            if not movable_pawns:
                val, _ = self.expectiminimax(state, depth - 1, True)
                return val, None

            if state.current_player == self.ai_color:
                best_val = -math.inf
                best_move = None
                for p_id in movable_pawns:
                    # محاكاة الحركة
                    new_board = deepcopy(board)
                    new_board.handle_movement(p_id, current_dice)
                    next_state = GameState(new_board, new_board.current_player)
                    
                    val, _ = self.expectiminimax(next_state, depth - 1, True)
                    if val > best_val:
                        best_val = val
                        best_move = p_id
                return best_val, best_move
            else:
                best_val = math.inf
                best_move = None
                for p_id in movable_pawns:
                    new_board = deepcopy(board)
                    new_board.handle_movement(p_id, current_dice)
                    next_state = GameState(new_board, new_board.current_player)
                    
                    val, _ = self.expectiminimax(next_state, depth - 1, True)
                    if val < best_val:
                        best_val = val
                        best_move = p_id
                return best_val, best_move