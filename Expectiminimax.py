import math
from ThrowingSticks import stick_throw_probabilities
from copy import deepcopy
from GameState import GameState


class Expectiminimax:
    def __init__(self, depth, ai_color="WHITE"):
        self.max_depth = depth
        self.ai_color = ai_color
        self.opponent_color = "BLACK" if ai_color == "WHITE" else "WHITE"
        self.nodes_count = 0
        self.log_file = "ai_search_log.txt"

    # def evaluate_heuristic(self, state):
    #     score = 0
    #     board = state.board

    #     if board.is_game_over():
    #         winner = board.get_winner()
    #         if winner == self.ai_color: return 10000
    #         else: return -10000
    #     score += (board.exited_pawns[self.ai_color] * 200)
    #     score -= (board.exited_pawns[self.opponent_color] * 200)

    #     for pawn in board.get_pawns_of_player(self.ai_color):
    #         if pawn.cell_id is not None:
    #             score += pawn.cell_id
    #             if pawn.cell_id in [26, 30]: score += 150
    #             elif pawn.cell_id == 27: score -= 100
    #             elif pawn.cell_id == 28:
    #                 score += (100 - (12/16) * (28 - 15))
    #             elif pawn.cell_id == 29:
    #                 score += (100 - (10/16) * (29 - 15))
    #     for pawn in board.get_pawns_of_player(self.opponent_color):
    #         if pawn.cell_id is not None:
    #             score -= pawn.cell_id
    #             if pawn.cell_id in [26, 30]: score -= 150
    #             elif pawn.cell_id == 27: score += 100
    #             elif pawn.cell_id == 28:
    #                 score -= (100 - (12/16) * (28 - 15))
    #             elif pawn.cell_id == 29:
    #                 score -= (100 - (10/16) * (29 - 15))

    #     if board.current_player == self.opponent_color:
    #        dice_to_check = board.current_dice if board.current_dice else 1
    #        movable_pawns = board.get_movable_pawns(dice_to_check)

    #        if not movable_pawns:
    #           score += 100

    #     return score

    def evaluate_heuristic(self, state):
        score = 0
        board = state.board

        if board.is_game_over():
            winner = board.get_winner()
            if winner == self.ai_color:
                return 10000
            else:
                return -10000

        score += (board.exited_pawns[self.ai_color] * 200)
        score -= (board.exited_pawns[self.opponent_color] * 200)

        for pawn in board.get_pawns_of_player(self.ai_color):
            if pawn.cell_id is not None:
                score += pawn.cell_id

                if pawn.cell_id == 30:
                    score += 500
                elif pawn.cell_id == 26:
                    score += 100
                elif pawn.cell_id == 27:
                    score -= 100
                elif pawn.cell_id == 28:
                    # score += 48.75
                    # (500 * 4/16) + (15 * 12/16)
                    score += 136.25
                elif pawn.cell_id == 29:
                    # score +=65.625
                    # (500 * 6/16) + (15 * 10/16)
                    score += 196.875

        for pawn in board.get_pawns_of_player(self.opponent_color):
            if pawn.cell_id is not None:
                score -= pawn.cell_id

                if pawn.cell_id == 30:
                    score -= 500
                elif pawn.cell_id == 26:
                    score -= 100
                elif pawn.cell_id == 27:
                    score += 100
                elif pawn.cell_id == 28:
                    # score -= 48.75
                    score -= 136.25
                elif pawn.cell_id == 29:
                    # score -=65.625
                    score -= 196.875

        if board.current_player == self.opponent_color:
            dice_to_check = board.current_dice if board.current_dice else 1
            movable_pawns = board.get_movable_pawns(dice_to_check)

            if not movable_pawns:
                score += 100

        return score

    # def expectiminimax(self, state, depth, is_chance_node, current_dice=None):
    #     if depth == 0 or state.board.is_game_over():
    #         return self.evaluate_heuristic(state), None

    #     if is_chance_node:
    #         expected_value = 0
    #         probs = stick_throw_probabilities()
    #         for dice_val, prob in probs.items():
    #             val, _ = self.expectiminimax(state, depth - 1, False, dice_val)
    #             expected_value += prob * val
    #         return expected_value, None

    #     else:
    #         board = state.board
    #         movable_pawns = board.get_movable_pawns(current_dice)

    #         if not movable_pawns:
    #             val, _ = self.expectiminimax(state, depth - 1, True)
    #             return val, None

    #         if state.current_player == self.ai_color:
    #             best_val = -math.inf
    #             best_move = None
    #             for p_id in movable_pawns:
    #                 # محاكاة الحركة
    #                 new_board = deepcopy(board)
    #                 new_board.handle_movement(p_id, current_dice)
    #                 next_state = GameState(new_board, new_board.current_player)

    #                 val, _ = self.expectiminimax(next_state, depth - 1, True)
    #                 if val > best_val:
    #                     best_val = val
    #                     best_move = p_id
    #             return best_val, best_move
    #         else:
    #             best_val = math.inf
    #             best_move = None
    #             for p_id in movable_pawns:
    #                 new_board = deepcopy(board)
    #                 new_board.handle_movement(p_id, current_dice)
    #                 next_state = GameState(new_board, new_board.current_player)

    #                 val, _ = self.expectiminimax(next_state, depth - 1, True)
    #                 if val < best_val:
    #                     best_val = val
    #                     best_move = p_id
    #             return best_val, best_move

    def expectiminimax(self, state, depth, is_chance_node, current_dice=None, indent=""):
        # زيادة عداد العقد عند زيارة كل عقدة جديدة
        self.nodes_count += 1

        # تحضير معلومات العقدة لطباعتها في الملف
        node_type = "CHANCE" if is_chance_node else (
            "MAX" if state.current_player == self.ai_color else "MIN")
        log_entry = f"{indent}Node: {node_type}, Depth: {depth}, Dice: {current_dice}\n"

        # كتابة المعلومات في الملف
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)

        # حالة النهاية (حالة فوز أو وصول لأقصى عمق)
        if depth == 0 or state.board.is_game_over():
            score = self.evaluate_heuristic(state)
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"{indent}Reached Leaf - Value: {score}\n")
            return score, None

        if is_chance_node:
            expected_value = 0
            probs = stick_throw_probabilities()

            for dice_val, prob in probs.items():
                val, _ = self.expectiminimax(
                    state, depth - 1, False, dice_val, indent + "  ")
                expected_value += prob * val

            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"{indent}Chance Node Result: {expected_value}\n")
            return expected_value, None

        else:
            board = state.board
            movable_pawns = board.get_movable_pawns(current_dice)

            if not movable_pawns:
                val, _ = self.expectiminimax(
                    state, depth - 1, True, None, indent + "  ")
                return val, None

            if state.current_player == self.ai_color:
                best_val = -math.inf
                best_move = None
                for p_id in movable_pawns:
                    new_board = deepcopy(board)
                    new_board.handle_movement(p_id, current_dice)
                    next_state = GameState(new_board, new_board.current_player)

                    val, _ = self.expectiminimax(
                        next_state, depth - 1, True, None, indent + "  ")
                    if val > best_val:
                        best_val = val
                        best_move = p_id

                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(f"{indent}MAX Node Best Value: {best_val}\n")
                return best_val, best_move
            else:
                best_val = math.inf
                best_move = None
                for p_id in movable_pawns:
                    new_board = deepcopy(board)
                    new_board.handle_movement(p_id, current_dice)
                    next_state = GameState(new_board, new_board.current_player)

                    val, _ = self.expectiminimax(
                        next_state, depth - 1, True, None, indent + "  ")
                    if val < best_val:
                        best_val = val
                        best_move = p_id

                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(f"{indent}MIN Node Best Value: {best_val}\n")
                return best_val, best_move
